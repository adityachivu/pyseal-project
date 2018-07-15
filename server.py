import socket
import os
from _thread import *
import hashlib

serversock = socket.socket()
host = socket.gethostname();
port = 9005;
serversock.bind((host,port));
filename = ""
serversock.listen(100);
print("Waiting for a connection.....")


def recv_CipherMatrix(socket, path):
    """

    :param path:
    :return:
    """
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

def send_CipherMatrix(socket, path):
    """

    :param socket:
    :param path:
    :return:
    """

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


# while(True):
    # size = clientsocket.recv(16) # Note that you limit your filename length to 255 bytes.

clientsocket,addr = serversock.accept()
print("Got a connection from %s" % str(addr))
result = recv_CipherMatrix(clientsocket, "/seal-project/receive/")
print(result)

clientsocket,addr = serversock.accept()
print("Got a connection from %s" % str(addr))
result = recv_CipherMatrix(clientsocket, "/seal-project/receive2/")
print(result)


clientsocket,addr = serversock.accept()
print("Got a connection from %s" % str(addr))
send_CipherMatrix(clientsocket, "/seal-project/result/")

input("Press Enter to exit")



serversock.close()


