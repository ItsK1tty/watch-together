import socket
import ssl

MAX_CLIENT = 10

state = ["Hello", "Auth", "AuthSuccess" "InvalidAuth", "WatchJoin", "Watching", "Terminated"]
testCreds = [["test", "test"]]
def server_program():
    # get the hostname
    host = "localhost" #socket.gethostname()
    port = 12545  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server = ssl.wrap_socket(
    server, server_side=True, keyfile="path/to/keyfile", certfile="path/to/certfile"
)
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(MAX_CLIENT)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        if data == "Client Hello":
            curState = state[0]
            msg = "Server Hello|Auth"
            conn.send(msg.encode())
        elif "Client Auth{" in data: # Client Auth{login|password}
            curState = state[1]
            msg = data.split("{", 1)[1][:-1]
            creds = msg.split("|", 1)
            loginCred = creds[0]
            passCred = creds[1]
            if [loginCred, passCred] in testCreds:
                conn.send("auth Success".encode())
                curState = state[2]
            else:
                conn.send("auth Failure".encode())
                curState = state[3]
                conn.close()

        #conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()

# taken from: https://digitalocean.com/community/tutorials/python-socket-programming-server-client