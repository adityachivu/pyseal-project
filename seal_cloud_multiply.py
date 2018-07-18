import ahem
import os


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
    ahem.recv_CipherMatrix(clientsocket, A_path)
    # print(result)

    clientsocket, addr = serversock.accept()
    print("Got a connection from %s" % str(addr))
    ahem.recv_CipherMatrix(clientsocket, B_path)
    # print(result)

    A = ahem.CipherMatrix()
    A.load(A_path)

    B = ahem.CipherMatrix()
    B.load(B_path)

    res = A * B

    for file in os.listdir(A_path):
        os.remove(os.path.join(A_path, file))
    for file in os.listdir(B_path):
        os.remove(os.path.join(B_path, file))

    result_path = res.save(root_path)

    clientsocket, addr = serversock.accept()
    print("Got a connection from %s" % str(addr))
    ahem.send_CipherMatrix(clientsocket, result_path)

    close_server = int(input("Press Enter to exit"))




def main():

    print("SEAL MULTIPLY SERVER")
    ahem.PORT = int(input("Enter port:"))

    serversock = ahem.setup_server(ahem.PORT)

    close_server = True
    while(close_server):
        process_multiply_request(serversock)

    serversock.close()

if __name__ == "__main__":
    main()
