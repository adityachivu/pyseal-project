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
    s.close()

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
    s.close()

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
    s.close()

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


def classify_request(img):
    """

    :param img:
    :return:
    """
    assert isinstance(img, CipherMatrix), "Input must be CipherMatrix"

    s = socket.socket()
    s.connect((basic.HOST, basic.PORT))
    s.send("classify".encode())
    s.close()

    keygen = img.get_keygen()

    local_path = "/seal-project/save/"
    img_path = img.save(local_path)

    s = socket.socket()
    s.connect((basic.HOST, basic.PORT))
    send_CipherMatrix(s, img_path)

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

    hidden = result.decrypt(keygen = keygen)

    import numpy as np
    hidden = 1 / (1 + np.exp(-hidden))

    hidden = CipherMatrix(hidden)
    hidden.encrypt(keygen=keygen)

    hidden_path = hidden.save(local_path)

    s = socket.socket()
    s.connect((basic.HOST, basic.PORT))
    send_CipherMatrix(s, hidden_path)

    s = socket.socket()
    s.connect((basic.HOST, basic.PORT))
    recv_CipherMatrix(s, result_path)

    result = CipherMatrix()
    result.load(result_path)

    for file in os.listdir(result_path):
        os.remove(os.path.join(result_path, file))

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


def process_classify_request(serversock):
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

    img = CipherMatrix()
    img.load(A_path)

    import numpy as np
    weights1 = np.load(root_path+'w1.npy')
    b1 = np.load(root_path+'b1.npy')
    weights2 = np.load(root_path+'w2.npy')
    b2 = np.load(root_path+'b2.npy')

    W1 = CipherMatrix(weights1)


    res = img * W1
    b1 = CipherMatrix(b1 * np.ones(shape=res.encrypted_matrix.shape))

    res = res + b1

    result_path = res.save(root_path)

    clientsocket, addr = serversock.accept()
    print("Got a connection from %s" % str(addr))
    send_CipherMatrix(clientsocket, result_path)

    clientsocket, addr = serversock.accept()
    print("Got a connection from %s" % str(addr))
    recv_CipherMatrix(clientsocket, B_path)

    hidden = CipherMatrix()
    hidden.load(B_path)

    W2 = CipherMatrix(weights2)
    res = hidden * W2
    b2= CipherMatrix(b2 * np.ones(shape=res.encrypted_matrix.shape))

    res = res + b2

    result_path = res.save(root_path)

    clientsocket, addr = serversock.accept()
    print("Got a connection from %s" % str(addr))
    send_CipherMatrix(clientsocket, result_path)

    for file in os.listdir(A_path):
        os.remove(os.path.join(A_path, file))
    for file in os.listdir(B_path):
        os.remove(os.path.join(B_path, file))