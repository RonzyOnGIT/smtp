# Although smtp servers, can serve as clients and servers, for purpose of this project, this simplified smtp server will be strictly used as a server
from socket import *
import sys

serverPort = 1025

# make socket that uses IPv4 and TCP
serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(("", serverPort))

serverSocket.listen(1)

print("Server ready for requests")

while True:
    # after this line, succesfully established TCP connection with client, send 220 message
    connectionSocket, userAddress = serverSocket.accept()


    # 220 greeting
    introductionMessage = "220 dummyserver.com Simple Mail Server\r\n"
    connectionSocket.send(introductionMessage.encode())

    # Wait for client to send HELO
    clientMessage = connectionSocket.recv(1024).decode()

    if (clientMessage[:4] != 'HELO'):
        print("500")
        sys.exit()

    greetingMessage = "250 Hello " + clientMessage[5:]
    connectionSocket.send(greetingMessage.encode())

    

    # introduction
    message = "220 dummyserver.com"
    # user sends helo message and their server



