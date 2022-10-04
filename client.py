import socket
import ssl

loginCred = "test"
passCred = "test"


def client_program():
    host = "localhost"  # as both code is running on same pc
    port = 12545  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sslsocket = ssl.wrap_socket(client_socket)

    sslsocket.connect((host, port))  # connect to the server
    message = "Client Hello"

    while message.lower().strip() != 'bye':
        if message != "waiting":
            sslsocket.send(message.encode())  # send message
        data = sslsocket.recv(1024).decode()  # receive response

        if data == "Server Hello|Auth":
            message = "Client Auth{"+loginCred+"|"+passCred+"}"
            #sslsocket.send(message.encode())
        elif data == "auth Success":
            print("Auth success")
            message = "MovieSync"
        elif data == "auth Failure":
            print("Auth failed")
            break
        elif "MovieSync|" in data:
            print(data)
            message = "waiting"
        
            


        #message = input(" -> ")  # again take input

    sslsocket.shutdown(socket.SHUT_RDWR)
    sslsocket.close()
    client_socket.close()


if __name__ == '__main__':
    client_program()