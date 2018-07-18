import numpy as np
import os
import seal
from seal import ChooserEvaluator,     \
                 Ciphertext,           \
                 Decryptor,            \
                 Encryptor,            \
                 EncryptionParameters, \
                 Evaluator,            \
                 IntegerEncoder,       \
                 FractionalEncoder,    \
                 KeyGenerator,         \
                 MemoryPoolHandle,     \
                 Plaintext,            \
                 SEALContext,          \
                 EvaluationKeys,       \
                 GaloisKeys,           \
                 PolyCRTBuilder,       \
                 ChooserEncoder,       \
                 ChooserEvaluator,     \
                 ChooserPoly

from . import *


class CipherMatrix:
    """

    """
    def __init__(self, matrix = None):
        """

        :param matrix: numpy.ndarray to be encrypted.
        """

        self.parms = EncryptionParameters()
        self.parms.set_poly_modulus("1x^2048 + 1")
        self.parms.set_coeff_modulus(seal.coeff_modulus_128(2048))
        self.parms.set_plain_modulus(1 << 8)

        self.context = SEALContext(self.parms)

        # self.encoder = IntegerEncoder(self.context.plain_modulus())
        self.encoder = FractionalEncoder(self.context.plain_modulus(), self.context.poly_modulus(), 64, 32, 3)

        self.keygen = KeyGenerator(self.context)
        self.public_key = self.keygen.public_key()
        self.secret_key = self.keygen.secret_key()

        self.encryptor = Encryptor(self.context, self.public_key)
        self.decryptor = Decryptor(self.context, self.secret_key)

        self.evaluator = Evaluator(self.context)

        self._saved = False
        self._encrypted = False
        self._id = '{0:04d}'.format(np.random.randint(1000))

        if matrix is not None:
            assert len(matrix.shape) == 2, "Only 2D numpy matrices accepted currently"
            self.matrix = np.copy(matrix)
            self.encrypted_matrix = np.empty(self.matrix.shape, dtype=object)
            for i in range(self.matrix.shape[0]):
                for j in range(self.matrix.shape[1]):
                    self.encrypted_matrix[i,j] = Ciphertext()

        else:
            self.matrix = None
            self.encrypted_matrix = None

        print(self._id, "Created")


    def __repr__(self):
        """

        :return:
        """
        print("Encrypted:", self._encrypted)
        if not self._encrypted:
            print(self.matrix)
            return ""

        else:
            return '[]'

    def __str__(self):
        """

        :return:
        """
        print("| Encryption parameters:")
        print("| poly_modulus: " + self.context.poly_modulus().to_string())

        # Print the size of the true (product) coefficient modulus
        print("| coeff_modulus_size: " + (str)(self.context.total_coeff_modulus().significant_bit_count()) + " bits")

        print("| plain_modulus: " + (str)(self.context.plain_modulus().value()))
        print("| noise_standard_deviation: " + (str)(self.context.noise_standard_deviation()))

        if self.matrix is not None:
            print(self.matrix.shape)

        return str(type(self))

    def __add__(self, other):
        """

        :param other:
        :return:
        """
        assert isinstance(other, CipherMatrix), "Can only be added with a CipherMatrix"

        A_enc = self._encrypted
        B_enc = other._encrypted

        if A_enc:
            A = self.encrypted_matrix
        else:
            A = self.matrix

        if B_enc:
            B = other.encrypted_matrix
        else:
            B = other.matrix

        assert A.shape == B.shape, "Dimension mismatch, Matrices must be of same shape"

        shape = A.shape

        result = CipherMatrix(np.zeros(shape, dtype=np.int32))
        result._update_cryptors(self.get_keygen())

        if A_enc:
            if B_enc:

                res_mat = result.encrypted_matrix
                for i in range(shape[0]):
                    for j in range(shape[1]):
                        self.evaluator.add(A[i,j], B[i,j], res_mat[i,j])

                result._encrypted = True

            else:
                res_mat = result.encrypted_matrix
                for i in range(shape[0]):
                    for j in range(shape[1]):
                        self.evaluator.add_plain(A[i, j], self.encoder.encode(B[i, j]), res_mat[i, j])

                result._encrypted = True

        else:
            if B_enc:

                res_mat = result.encrypted_matrix
                for i in range(shape[0]):
                    for j in range(shape[1]):
                        self.evaluator.add_plain(B[i, j], self.encoder.encode(A[i, j]), res_mat[i, j])

                result._encrypted = True

            else:

                result.matrix = A + B
                result._encrypted = False

        return result


    def __sub__(self, other):
        """

        :param other:
        :return:
        """
        assert isinstance(other, CipherMatrix)
        if other._encrypted:
            shape = other.encrypted_matrix.shape

            for i in range(shape[0]):
                for j in range(shape[1]):
                    self.evaluator.negate(other.encrypted_matrix[i,j])

        else:
            other.matrix = -1 * other.matrix

        return self + other

    def __mul__(self, other):
        """

        :param other:
        :return:
        """

        assert isinstance(other, CipherMatrix), "Can only be multiplied with a CipherMatrix"

        # print("LHS", self._id, "RHS", other._id)
        A = self.encrypted_matrix
        B = other.encrypted_matrix

        Ashape = A.shape
        Bshape = B.shape

        assert Ashape[1] == Bshape[0], "Dimensionality mismatch"
        result_shape = [Ashape[0], Bshape[1]]

        result = CipherMatrix()
        result.encrypted_matrix = np.empty(result_shape, dtype=object)

        for i in range(Ashape[0]):
            for j in range(Bshape[1]):

                result_array = []
                for k in range(Ashape[1]):

                    res = Ciphertext()
                    self.evaluator.multiply(A[i, k], B[k, j], res)

                    result_array.append(res)

                result.encrypted_matrix[i, j] = Ciphertext()
                self.evaluator.add_many(result_array, result.encrypted_matrix[i,j])

        result._encrypted = True

        return result

    def save(self, path):
        """

        :param path:
        :return:
        """

        save_dir = os.path.join(path, self._id)

        if self._saved:
            print("CipherMatrix already saved")

        else:
            assert not os.path.isdir(save_dir), "Directory already exists"
            os.mkdir(save_dir)

        if not self._encrypted:
            self.encrypt()

        shape = self.encrypted_matrix.shape

        for i in range(shape[0]):
            for j in range(shape[1]):
                # print('saving', i, '-', j)
                element_name = str(i)+'-'+str(j)+'.ahem'
                self.encrypted_matrix[i,j].save(os.path.join(save_dir, element_name))

        self.secret_key.save("/keys/"+"."+self._id+'.wheskey')

        self._saved = True
        return save_dir

    def load(self, path, load_secret_key = False):
        """

        :param path:
        :param load_secret_key:
        :return:
        """

        self._id = path.split('/')[-1]
        print("Loading Matrix:", self._id)

        file_list = os.listdir(path)
        index_list = [[file.split('.')[0].split('-'), file] for file in file_list]

        M = int(max([ind[0][0] for ind in index_list])) + 1
        N = int(max([ind[0][1] for ind in index_list])) + 1

        del self.encrypted_matrix
        self.encrypted_matrix = np.empty([M, N], dtype=object)

        for index in index_list:
            i = int(index[0][0])
            j = int(index[0][1])

            self.encrypted_matrix[i,j] = Ciphertext()
            self.encrypted_matrix[i,j].load(os.path.join(path, index[1]))

        if load_secret_key:
            self.secret_key.load("/keys/"+"."+self._id+'.wheskey')

        self.matrix = np.empty(self.encrypted_matrix.shape)
        self._encrypted = True

    def encrypt(self, matrix = None, keygen = None):
        """

        :param matrix:
        :return:
        """

        assert not self._encrypted, "Matrix already encrypted"

        if matrix is not None:
            assert self.matrix is None, "matrix already exists"
            self.matrix = np.copy(matrix)

        shape = self.matrix.shape

        self.encrypted_matrix = np.empty(shape, dtype = object)

        if keygen is not None:
            self._update_cryptors(keygen)

        for i in range(shape[0]):
            for j in range(shape[1]):
                val = self.encoder.encode(self.matrix[i,j])
                self.encrypted_matrix[i,j] = Ciphertext()
                self.encryptor.encrypt(val, self.encrypted_matrix[i,j])

        self._encrypted = True

    def decrypt(self, encrypted_matrix = None, keygen = None):
        """

        :return:
        """

        if encrypted_matrix is not None:
            self.encrypted_matrix = encrypted_matrix

        assert self._encrypted, "No encrypted matrix"

        del self.matrix
        shape = self.encrypted_matrix.shape

        self.matrix = np.empty(shape)

        if keygen is not None:
            self._update_cryptors(keygen)

        for i in range(shape[0]):
            for j in range(shape[1]):
                plain_text = Plaintext()
                self.decryptor.decrypt(self.encrypted_matrix[i,j], plain_text)
                self.matrix[i,j] = self.encoder.decode(plain_text)

        self._encrypted = False
        return np.copy(self.matrix)

    def get_keygen(self):
        """

        :return:
        """
        return self.keygen

    def _update_cryptors(self, keygen):
        """

        :param keygen:
        :return:
        """

        self.keygen = keygen
        self.public_key = keygen.public_key()
        self.secret_key = keygen.secret_key()

        self.encryptor = Encryptor(self.context, self.public_key)
        self.decryptor = Decryptor(self.context, self.secret_key)

        return


def test():
    print('----------------WELCOME TO AHEM-------------------')


def main():
    print("CipherMatrix class definition")


if __name__ == '__main__':
    main()