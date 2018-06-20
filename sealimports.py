import numpy as np
import seal


class CipherMatrix:

    def __init__(self, params = None, matrix = None):
        """

        :param self:
        :param matrix:
        :param encryptor:
        :return:
        """

        if params is not None:
            self.params = params

        if matrix is not None:
            assert params is not None, 'Parameters need to be provided, if matrix is provided'
            self.shape = matrix.shape
            self.ciphermat = np.empty(shape)
            self.encrypt(matrix)

        else:
            if params is not None:
                self.params = params
            self.shape = None
            self.ciphermat = None


    def encrypt(self, matrix):
        """

        :param matrix:
        :return:
        """

        self.context =

        self.secret_key
        self.public_key
        [m, n] = self.shape

        for i in range(m):
            for j in range(n):
                self.ciphermat[i,j] = seal.Ciphertext(self.params)
                self.ciphermat[i,j] =

