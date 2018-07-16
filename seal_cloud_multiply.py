import ahem
import os


def process_multiply_request():
    """

    :return:
    """
    clientsocket, addr = serversock.accept()
    print("Got a connection from %s" % str(addr))
    result = recv_CipherMatrix(clientsocket, "/seal-project/receive/")
    print(result)

    clientsocket, addr = serversock.accept()
    print("Got a connection from %s" % str(addr))
    result = recv_CipherMatrix(clientsocket, "/seal-project/receive2/")
    print(result)

    clientsocket, addr = serversock.accept()
    print("Got a connection from %s" % str(addr))
    send_CipherMatrix(clientsocket, "/seal-project/result/")




def main():
    print("SEAL MULTIPLY SERVER")
    ahem.PORT = int(input("Enter post number:"))

    serversock = ahem.setup_server(ahem.PORT)

    root_path = "/seal-project/server/"

    A_path = "/seal-project/server/A/"
    clientsocket, addr = serversock.accept()
    print("Got a connection from %s" % str(addr))
    ahem.recv_CipherMatrix(clientsocket, A_path)
    # print(result)

    B_path = "/seal-project/server/B/"
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
        os.remove(os.path.join(A_path,file))
    for file in os.listdir(B_path):
        os.remove(os.path.join(B_path,file))

    result_path = res.save("/seal-project/server/")

    clientsocket, addr = serversock.accept()
    print("Got a connection from %s" % str(addr))
    ahem.send_CipherMatrix(clientsocket, result_path)

    input("Press Enter to exit")

    serversock.close()

if __name__ == "__main__":
    main()
