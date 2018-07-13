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
        self.parms.set_poly_modulus("1x^2048 + 1")
        self.parms.set_coeff_modulus(seal.coeff_modulus_128(2048))
        self.parms.set_plain_modulus(1 << 8)

        self.context = SEALContext(self.parms)

        self.encoder = IntegerEncoder(self.context.plain_modulus())

        self.keygen = KeyGenerator(self.context)
        self.public_key = self.keygen.public_key()
        self.secret_key = self.keygen.secret_key()

        self.encryptor = Encryptor(self.context, self.public_key)
        self.decryptor = Decryptor(self.context, self.secret_key)



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
            assert self.matrix is not None, "matrix already exists"
            self.matrix = np.copy(matrix)

        shape = self.matrix.shape

        self.encrypted_matrix = np.empty(shape, dtype = object)

        for i in range(shape[0]):
            for j in range(shape[1]):
                val = self.encoder.encode(self.matrix[i,j])
                self.encrypted_matrix[i,j] = Ciphertext()
                self.encryptor.encrypt(val, self.encrypted_matrix[i,j])

    def decrypt(self):
        """

        :return:
        """

        assert self.encrypted_matrix is not None, "No encrypted matrix"
        del self.matrix
        shape = self.encrypted_matrix.shape

        self.matrix = np.empty(shape)

        for i in range(shape[0]):
            for j in range(shape[1]):
                plain_text = Plaintext()
                self.decryptor.decrypt(self.encrypted_matrix[i,j], plain_text)
                self.matrix[i,j] = self.encoder.decode_int32(plain_text)

        return self.matrix

def test():
    print('blah')