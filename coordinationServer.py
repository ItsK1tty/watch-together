import socket
import ssl
import _thread
import os
from pymongo import MongoClient

MOVIE_PATH = "C://movie_test"

groupStarted = False
groupMembers = []

def getAvailableMovies():
    result = ""
    for item in os.listdir(MOVIE_PATH):
        moviePath = os.path.join(MOVIE_PATH, item)
        if os.path.isdir(moviePath):
            result += item + "{"
            for file in os.listdir(moviePath):
                result += file + ","
            result = result[:-1]+"},"
    result = result[:-1]
    return result


def on_new_client(conn,addr):
    authed = False
    while True:
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        if data == "Client Hello":
            curState = states[0]
            msg = "Server Hello|Auth"
            conn.send(msg.encode())
        elif "Client Auth{" in data: # Client Auth{login|password}
            curState = states[1]
            msg = data.split("{", 1)[1][:-1]
            creds = msg.split("|", 1)
            loginCred = creds[0]
            passCred = creds[1]
            if [loginCred, passCred] in testCreds:
                conn.send("auth Success".encode())
                authed = True
                curState = states[2]
            else:
                conn.send("auth Failure".encode())
                curState = states[3]
                conn.close()
        elif data == "MovieSync" and authed:
            curState = states[4]
            message = "MovieSync|" + getAvailableMovies()
            conn.send(message.encode())
            print(message)
        elif data == "bye":
            curState = states[7]
            conn.send("bye".encode())
    conn.close()  # close the connection

MAX_CLIENT = 10

states = ["Hello", "Auth", "AuthSuccess", "InvalidAuth", "Synchronizing", "WatchJoin", "Watching", "Terminated"]
testCreds = [["test", "test"]]
def server_program():
    # get the hostname
    host = "localhost" #socket.gethostname()
    port = 12545  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket = ssl.wrap_socket(
    server_socket, server_side=True, keyfile="server.key", certfile="server.crt"
)
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(MAX_CLIENT)
    
    
    while True:
        conn, address = server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))
        _thread.start_new_thread(on_new_client,(conn,address))
    server_socket.close()



if __name__ == '__main__':
    server_program()

# taken from: https://digitalocean.com/community/tutorials/python-socket-programming-server-client