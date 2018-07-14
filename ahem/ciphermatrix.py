import numpy as np
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


class CipherMatrix:
    """

    """
    def __init__(self, matrix = None):
        """

        :param matrix: numpy.ndarray to be encrypted.
        """

        self.parms = EncryptionParameters()
        self.parms.set_poly_modulus("1x^8192 + 1")
        self.parms.set_coeff_modulus(seal.coeff_modulus_128(8192))
        self.parms.set_plain_modulus(1 << 8)

        self.context = SEALContext(self.parms)

        self.encoder = IntegerEncoder(self.context.plain_modulus())
        self.floatencoder = FractionalEncoder(self.context.plain_modulus(), self.context.poly_modulus(), 64, 32, 3)

        self.keygen = KeyGenerator(self.context)
        self.public_key = self.keygen.public_key()
        self.secret_key = self.keygen.secret_key()

        self.encryptor = Encryptor(self.context, self.public_key)
        self.decryptor = Decryptor(self.context, self.secret_key)

        self.evaluator = Evaluator(self.context)

        self._encrypted = False

        if matrix is not None:
            assert len(matrix.shape) == 2, "Only 2D numpy matrices accepted currently"
            self.matrix = np.copy(matrix)
            self.encrypted_matrix = None
            self.encrypt()

        else:
            self.matrix = None
            self.encrypted_matrix = None


    def __repr__(self):
        """

        :return:
        """
        if self.matrix is not None:
            return self.matrix

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

    def __mul__(self, other):
        """

        :param other:
        :return:
        """

        assert isinstance(other, CipherMatrix), "Can only be multiplied with a cipher matrix"

        result = CipherMatrix()

        A = self.encrypted_matrix
        B = other.encrypted_matrix

        # A = self.matrix
        # B = other.matrix

        Ashape = A.shape
        Bshape = B.shape

        assert Ashape[1] == Bshape[0], "Dimensionality mismatch"
        result_shape = [Ashape[0], Bshape[1]]

        result = CipherMatrix(np.zeros(result_shape, dtype=np.int32))
        plain_result = np.zeros(result_shape, dtype=np.int32)

        for i in range(Ashape[0]):
            for j in range(Bshape[1]):
                val = Ciphertext(self.parms)
                self.encryptor.encrypt(self.encoder.encode(0), val)

                result_array = []
                for k in range(Ashape[1]):
                    res = Ciphertext(self.parms)
                    result_array.append(res)
                    print("Noise budget in val: " + (str)(
                        self.decryptor.invariant_noise_budget(res)) + " bits")
                    self.evaluator.multiply(A[i, k], B[k, j], result_array[k])
                    print(i, j, k)


                    # self.evaluator.add(val, res)
                    del res

                    #
                    #
                    # temp = A[i,k] * B[k,j]
                    # plain_result[i,j] = plain_result[i,j] + temp
                    #


                self.evaluator.add_many(result_array, val)
                self.evaluator.add(result.encrypted_matrix[i,j], val)


        return result
        # return plain_result

    def save(self, path):
        """

        :param path:
        :return:
        """
        pass

    def load(self, path):
        """

        :param path:
        :return:
        """
        pass

    def encrypt(self, matrix = None):
        """

        :param matrix:
        :return:
        """

        if matrix is not None:
            assert self.matrix is None, "matrix already exists"
            self.matrix = np.copy(matrix)

        shape = self.matrix.shape

        self.encrypted_matrix = np.empty(shape, dtype = object)

        for i in range(shape[0]):
            for j in range(shape[1]):
                val = self.encoder.encode(self.matrix[i,j])
                self.encrypted_matrix[i,j] = Ciphertext()
                self.encryptor.encrypt(val, self.encrypted_matrix[i,j])

        self._encrypted = True

    def decrypt(self):
        """

        :return:
        """

        assert self._encrypted and self.encrypted_matrix is not None, "No encrypted matrix"
        del self.matrix
        shape = self.encrypted_matrix.shape

        self.matrix = np.empty(shape)

        for i in range(shape[0]):
            for j in range(shape[1]):
                plain_text = Plaintext()
                self.decryptor.decrypt(self.encrypted_matrix[i,j], plain_text)
                self.matrix[i,j] = self.encoder.decode_int32(plain_text)

        self._encrypted = False
        return np.copy(self.matrix)

def test():
    print('blah')