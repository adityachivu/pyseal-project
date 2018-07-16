import socket
import os
from _thread import *


host = "172.17.0.2"
print(host)
port = 9005

def send_CipherMatrix(path):
    """

    :param socket:
    :param path:
    :return:
    """
    s = socket.socket()
    s.connect((host, port))

    directory = os.listdir(path)
    for files in directory:
        print(files)
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

def recv_CipherMatrix(path):
    """

    :param path:
    :return:
    """

    s = socket.socket()
    s.connect((host, port))

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
        print("File received succesfully")

    socket.close()
    return True


path = "/seal-project/cloud/"




send_CipherMatrix(path)


path = "/seal-project/result_receive/"
recv_CipherMatrix(path)



