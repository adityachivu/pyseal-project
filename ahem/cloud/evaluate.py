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
    assert isinstance(A, CipherMatrix) and isinstance(B, CipherMatrix), "Operands must be of type CipherMatrix"

    s = socket.socket()
    s.connect((basic.HOST, basic.PORT))
    s.send("add".encode())

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
    result_path = local_path + "RES"
    if not os.path.isdir(result_path):
        os.mkdir(result_path)
    recv_CipherMatrix(s, result_path)

    result = CipherMatrix()
    result.load(result_path)

    for file in os.listdir(result_path):
        os.remove(os.path.join(result_path, file))

    return result


def sub_request(A, B):
    """

    :param A:
    :param B:
    :return:
    """
    assert isinstance(A, CipherMatrix) and isinstance(B, CipherMatrix), "Operands must be of type CipherMatrix"

    s = socket.socket()
    s.connect((basic.HOST, basic.PORT))
    s.send("subtract".encode())

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
    result_path = local_path + "RES"
    if not os.path.isdir(result_path):
        os.mkdir(result_path)
    recv_CipherMatrix(s, result_path)

    result = CipherMatrix()
    result.load(result_path)

    for file in os.listdir(result_path):
        os.remove(os.path.join(result_path, file))

    return result


def det_request(A):
    """

    :param A:
    :return:
    """
    assert isinstance(A, CipherMatrix), "Argument must be of type CipherMatrix"


def multiply_request(A, B, A_path = None, B_path = None, result_path = None):
    """

    :param A:
    :param B:
    :return:
    """
    # assert isinstance(A, CipherMatrix) and isinstance(B, CipherMatrix) and \
    #        basic.CLIENT_SETUP, "Operands must CipherMatrix objects only"
    s = socket.socket()
    s.connect((basic.HOST, basic.PORT))
    s.send("multiply".encode())

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


def process_add_request(serversock):
    """

    :param serversock:
    :return:
    """

    root_path = "/seal-project/server/"
    A_path = "/seal-project/server/A/"
    B_path = "/seal-project/server/B/"

    clientsocket, addr = serversock.accept()
    print("Got a connection from %s" % str(addr))
    recv_CipherMatrix(clientsocket, A_path)
    # print(result)

    clientsocket, addr = serversock.accept()
    print("Got a connection from %s" % str(addr))
    recv_CipherMatrix(clientsocket, B_path)
    # print(result)

    A = CipherMatrix()
    A.load(A_path)

    B = CipherMatrix()
    B.load(B_path)

    res = A + B

    for file in os.listdir(A_path):
        os.remove(os.path.join(A_path, file))
    for file in os.listdir(B_path):
        os.remove(os.path.join(B_path, file))

    result_path = res.save(root_path)

    clientsocket, addr = serversock.accept()
    print("Got a connection from %s" % str(addr))
    send_CipherMatrix(clientsocket, result_path)


def process_subtract_request(serversock):
    """

    :param serversock:
    :return:
    """

    root_path = "/seal-project/server/"
    A_path = "/seal-project/server/A/"
    B_path = "/seal-project/server/B/"

    clientsocket, addr = serversock.accept()
    print("Got a connection from %s" % str(addr))
    recv_CipherMatrix(clientsocket, A_path)
    # print(result)

    clientsocket, addr = serversock.accept()
    print("Got a connection from %s" % str(addr))
    recv_CipherMatrix(clientsocket, B_path)
    # print(result)

    A = CipherMatrix()
    A.load(A_path)

    B = CipherMatrix()
    B.load(B_path)

    res = A - B

    for file in os.listdir(A_path):
        os.remove(os.path.join(A_path, file))
    for file in os.listdir(B_path):
        os.remove(os.path.join(B_path, file))

    result_path = res.save(root_path)

    clientsocket, addr = serversock.accept()
    print("Got a connection from %s" % str(addr))
    send_CipherMatrix(clientsocket, result_path)


def process_multiply_request(serversock):
    """

    :param serversock:
    :return:
    """

    root_path = "/seal-project/server/"
    A_path = "/seal-project/server/A/"
    B_path = "/seal-project/server/B/"

    clientsocket, addr = serversock.accept()
    print("Got a connection from %s" % str(addr))
    recv_CipherMatrix(clientsocket, A_path)
    # print(result)

    clientsocket, addr = serversock.accept()
    print("Got a connection from %s" % str(addr))
    recv_CipherMatrix(clientsocket, B_path)
    # print(result)

    A = CipherMatrix()
    A.load(A_path)

    B = CipherMatrix()
    B.load(B_path)

    res = A * B

    for file in os.listdir(A_path):
        os.remove(os.path.join(A_path, file))
    for file in os.listdir(B_path):
        os.remove(os.path.join(B_path, file))

    result_path = res.save(root_path)

    clientsocket, addr = serversock.accept()
    print("Got a connection from %s" % str(addr))
    send_CipherMatrix(clientsocket, result_path)
