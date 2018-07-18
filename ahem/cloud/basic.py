import socket
import os

HOST = ""
PORT = -1
CLIENT_SETUP = False

def setup_host(host, port):
    """

    :param host:
    :param port:
    :return:
    """
    global HOST
    global PORT
    global CLIENT_SETUP

    HOST = host
    PORT = port
    CLIENT_SETUP = True


def setup_server(port):
    """

    :param port:
    :return:
    """
    serversock = socket.socket()

    HOST = socket.gethostname()
    PORT = port

    serversock.bind((HOST, PORT))

    serversock.listen(100)
    print("Waiting for a connection.....")

    return serversock


def send_CipherMatrix(socket, path):
    """

    :param socket:
    :param path:
    :return:
    """
    directory = os.listdir(path)
    for files in directory:
        # print(files)
        filename = files
        size = len(filename)
        size = bin(size)[2:].zfill(16)  # encode filename size as 16 bit binary
        socket.send(size.encode())
        socket.send(filename.encode())

        filename = os.path.join(path, filename)
        filesize = os.path.getsize(filename)
        filesize = bin(filesize)[2:].zfill(32)  # encode filesize as 32 bit binary
        socket.send(filesize.encode())

        file_to_send = open(filename, 'rb')

        l = file_to_send.read()
        socket.sendall(l)
        file_to_send.close()

    print('Directory Sent')
    socket.close()


def recv_CipherMatrix(socket, path):
    """

    :param path:
    :return:
    """

    #
    #     socket.close()
    #     print("error")
    #     return
    #
    # os.path.mkdir(path)

    filename =""
    while(True):
        size = socket.recv(16)  # Note that you limit your filename length to 255 bytes.
        if not size:
            break
        size = int(size, 2)
        filename = socket.recv(size)
        if filename == 'DONE':
            return True
        filesize = socket.recv(32)
        filesize = int(filesize, 2)
        os.chdir(path)
        file_to_write = open(filename, 'wb')
        chunksize = 4096
        while filesize > 0:
            if filesize < chunksize:
                chunksize = filesize
            data = socket.recv(chunksize)
            file_to_write.write(data)
            filesize -= len(data)

        file_to_write.close()
        # print("File received succesfully")

    socket.close()
