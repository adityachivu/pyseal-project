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
        self._id = '{0:04d}'.format(np.random.randint(1000))

        if matrix is not None:
            assert len(matrix.shape) == 2, "Only 2D numpy matrices accepted currently"
            self.matrix = np.copy(matrix)
            self.encrypted_matrix = None
            self.encrypt()

        else:
            self.matrix = None
            self.encrypted_matrix = None

        print(self._id, "Created")


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

        result = CipherMatrix()
        result.encrypt(np.zeros(result_shape, dtype=np.int32), other.get_keygen())
        plain_result = np.zeros(result_shape, dtype=np.int32)

        for i in range(Ashape[0]):
            for j in range(Bshape[1]):
                val = Ciphertext(self.parms)
                self.encryptor.encrypt(self.encoder.encode(0), val)

                result_array = Ashape[1] * [Ciphertext()]
                for k in range(Ashape[1]):
                    # res = Ciphertext()
                    # result_array.append(res)

                    self.evaluator.multiply(A[i, k], B[k, j], result_array[k])
                    print("Noise budget in val: " + (str)(
                        self.decryptor.invariant_noise_budget(result_array[k])) + " bits")
                    print(i, j, k)


                    # self.evaluator.add(val, res)


                    #
                    #
                    # temp = A[i,k] * B[k,j]
                    # plain_result[i,j] = plain_result[i,j] + temp
                    #


                self.evaluator.add_many(result_array, val)
                self.evaluator.add(result.encrypted_matrix[i,j], val)

        # temp = Ciphertext(self.parms)
        #
        # self.evaluator.multiply(A[0,0], B[0,0], temp)
        #
        # # temp.decrypt()
        # plain_temp = Plaintext()
        #
        # self.decryptor.decrypt(A[0,0], plain_temp)
        # print(self.encoder.decode_int32(plain_temp))
        #
        # other.decryptor.decrypt(B[0,0], plain_temp)
        # print(self.encoder.decode_int32(plain_temp))
        #
        # other.decryptor.decrypt(temp, plain_temp)
        # return self.encoder.decode_int32(plain_temp)

        result.secret_key = other.keygen.secret_key()
        result.public_key = other.keygen.public_key()
        result.encryptor = Encryptor(result.context, result.public_key)
        result.decryptor = Decryptor(result.context, result.secret_key)
        return result
        # return plain_result

    def save(self, path):
        """

        :param path:
        :return:
        """

        if not self._encrypted:
            self.encrypt()

        shape = self.encrypted_matrix.shape

        save_dir = os.path.join(path, self._id)
        assert not os.path.isdir(save_dir), "Directory already exists"
        os.mkdir(save_dir)

        for i in range(shape[0]):
            for j in range(shape[1]):
                print('saving', i, '-', j)
                element_name = str(i)+'-'+str(j)+'.ahem'
                (self.encrypted_matrix[i,j]).save(os.path.join(save_dir, element_name))

        self.public_key.save("/keys/"+"."+self._id+'.whepkey')
        self.secret_key.save("/keys/"+"."+self._id+'.wheskey')

        return


    def load(self, path, keygen = None):
        """

        :param path:
        :return:
        """

        self.name = path.split('/')[-1]
        print(self.name)

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

        if keygen is None:
            key = seal.SecretKey()
            key.load('/keys/.'+self.name+'.wheskey')
            self.secret_key = key

            key = seal.PublicKey()
            key.load('/keys/.'+self.name+'.whepkey')
            self.public_key = key

            self.encryptor = Encryptor(self.context, self.public_key)
            self.decryptor = Decryptor(self.context, self.secret_key)

        else:


        self._encrypted = True

        print(M, N)
        print(index_list)


    def encrypt(self, matrix = None, keygen = None):
        """

        :param matrix:
        :return:
        """

        assert not self._encrypted and self.encrypted_matrix is None, "Matrix already encrypted"

        if matrix is not None:
            assert self.matrix is None, "matrix already exists"
            self.matrix = np.copy(matrix)

        shape = self.matrix.shape

        self.encrypted_matrix = np.empty(shape, dtype = object)

        if keygen is not None:
            self.public_key = keygen.public_key()
            self.secret_key = keygen.secret_key()
            self.encryptor = Encryptor(self.context, self.public_key)
            self.decryptor = Decryptor(self.context, self.secret_key)

        for i in range(shape[0]):
            for j in range(shape[1]):
                val = self.encoder.encode(self.matrix[i,j])
                self.encrypted_matrix[i,j] = Ciphertext()
                self.encryptor.encrypt(val, self.encrypted_matrix[i,j])

        del self.matrix
        self.matrix = None
        self._encrypted = True

    def decrypt(self, encrypted_matrix = None, keygen = None):
        """

        :return:
        """

        if encrypted_matrix is not None:
            self.encrypted_matrix = encrypted_matrix

        assert self._encrypted and self.matrix is None, "No encrypted matrix"

        del self.matrix
        shape = self.encrypted_matrix.shape

        self.matrix = np.empty(shape)

        if keygen is not None:
            self.public_key = keygen.public_key()
            self.secret_key = keygen.secret_key()
            self.encryptor = Encryptor(self.context, self.public_key)
            self.decryptor = Decryptor(self.context, self.secret_key)

        for i in range(shape[0]):
            for j in range(shape[1]):
                plain_text = Plaintext()
                self.decryptor.decrypt(self.encrypted_matrix[i,j], plain_text)
                self.matrix[i,j] = self.encoder.decode_int32(plain_text)

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
    print('blah')