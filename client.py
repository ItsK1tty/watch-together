import socket
import ssl

loginCred = "test"
passCred = "test"


def client_program():
    host = "localhost"  # as both code is running on same pc
    port = 12545  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    client_socket = ssl.wrap_socket(client_socket, keyfile="path/to/keyfile", certfile="path/to/certfile")

    client_socket.connect((host, port))  # connect to the server

    #message = input(" -> ")  # take input
    message = "Client Hello"

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        if data == "Server Hello|Auth":
            message = "Client Auth{"+loginCred+"|"+passCred+"}"
            client_socket.send(message.encode())
        elif data == "auth Success":
            print("Auth success")

        elif data == "auth Failure":
            print("Auth failed")
            client_socket.close()


        #message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()