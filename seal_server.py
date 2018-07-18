import ahem
import ahem.cloud as cloud
import os


def main():

    print("--------------------------PySEAL SERVER------------------------")
    ahem.PORT = int(input("Enter port:"))

    serversock = ahem.setup_server(ahem.PORT)

    close_server = False
    while(not close_server):
        # process_multiply_request(serversock)

        clientsocket, addr = serversock.accept()
        option = clientsocket.recv(16)
        option = option.decode()
        clientsocket.close()

        if option == "multiply":
            cloud.process_multiply_request(serversock)

        elif option == "add":
            cloud.process_add_request(serversock)

        elif option == "subtract":
            cloud.process_subtract_request(serversock)

        elif option == "classify":
            cloud.process_classify_request(serversock)

        elif option == "close":
            close_server = True

        print("Processed")

    serversock.close()

if __name__ == "__main__":
    main()
