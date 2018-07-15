from .. import ciphermatrix
from ..ciphermatrix import CipherMatrix


def add_request(A, B):
    """

    :param A:
    :param B:
    :return:
    """
    assert isinstance(A, CipherMatix) and isinstance(B, CipherMatrix), "Operands must be of type CipherMatrix"


def det_request(A):
    """

    :param A:
    :return:
    """
    assert isinstance(A, CipherMatix), "Argument must be of type CipherMatrix"


def classify_request(A):
    """

    :param A:
    :return:
    """

def multiply_request(A, B):