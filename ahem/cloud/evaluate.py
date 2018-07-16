from .. import ciphermatrix
from ..ciphermatrix import CipherMatrix

from . import basic
from .basic import *


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

def multiply_request(A, B, A_path = None, B_path = None, result_path = None):
    """

    :param A:
    :param B:
    :return:
    """
    # assert isinstance(A, CipherMatrix) and isinstance(B, CipherMatrix) and \
    #        basic.CLIENT_SETUP, "Operands must CipherMatrix objects only"

    local_path = "/seal-project/save/"
    A_path = A.save(local_path)
    B_path = B.save(local_path)

    s = socket.socket()
    s.connect((basic.HOST, basic.PORT))
    send_CipherMatrix(s, A_path)

    s = socket.socket()
    s.connect((basic.HOST, basic.PORT))
    send_CipherMatrix(s, B_path)

    s = socket.socket()
    s.connect((basic.HOST, basic.PORT))
    result_path = local_path+"RES"
    if not os.path.isdir(result_path):
        os.mkdir(result_path)
    recv_CipherMatrix(s, result_path)

    result = CipherMatrix()
    result.load(result_path)

    for file in os.listdir(result_path):
        os.remove(os.path.join(result_path,file))


    return result



