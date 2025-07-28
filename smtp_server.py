# Although smtp servers, can serve as clients and servers, for purpose of this project, this simplified smtp server will be strictly used as a server
# I plan to add threading in the future to allow for more than one client at a time

from socket import *
import sys

serverPort = 1025

# make socket that uses IPv4 and TCP
serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(("", serverPort))

serverSocket.listen(1)

print("Server ready for requests")

# have to add functionality so that if client sends 'QUIT' at any point, break close connection
while True:
    # after this line, succesfully established TCP connection with client, send 220 message
    connectionSocket, userAddress = serverSocket.accept()

    # 220 greeting
    introductionMessage = '220 dummyserver.com Simple Mail Server\r\n'
    connectionSocket.send(introductionMessage.encode())

    # Wait for client to send HELO
    clientHelo = connectionSocket.recv(1024).decode()

    if (clientHelo[:4] != 'HELO'):
        connectionSocket.send('500 error'.encode())
        connectionSocket.close()
        continue

    greetingMessage = '250 Hello ' + clientHelo[5:].strip() + ' pleased to meet you\r\n' 
    connectionSocket.send(greetingMessage.encode())

    clientMailFrom = connectionSocket.recv(1024).decode()

    if (clientMailFrom[:9] != 'MAIL FROM'):
        connectionSocket.send('no mail from'.encode())
        connectionSocket.close()
        continue
    

    # verify client
    closingBracketIndex = clientMailFrom.find('>')
    clientEmail = clientMailFrom[12:closingBracketIndex]

    verifiedClientMessage = '250 ' + clientEmail + ' ... Sender ok\r\n'
    connectionSocket.send(verifiedClientMessage.encode())

    # Destination email (rcpt)
    clientRcpt = connectionSocket.recv(1024).decode()

    if (clientRcpt[:7] != 'RCPT TO'):
        connectionSocket.send('500 error'.encode())
        connectionSocket.close()
        continue
    
    closingBracketIndex = clientRcpt.find('>')
    rcptEmail = clientRcpt[10:closingBracketIndex]

    rcptOkMessage = '250 ' + rcptEmail + ' ... ' + 'Recipient ok\r\n'
    connectionSocket.send(rcptOkMessage.encode())

    clientDataResponse = connectionSocket.recv(1024).decode()

    if (clientDataResponse.strip() != 'DATA'):
        connectionSocket.send('500 error'.encode())
        connectionSocket.close()
        continue

    clientDataMessage = '354 Enter mail, end with "." on a line by itself\r\n'
    connectionSocket.send(clientDataMessage.encode())


    clientEmailContent = ''
    while True:
        clientDataBodyResponse = connectionSocket.recv(1024).decode()
        if (clientDataBodyResponse == '.\r\n'):
            break
        clientEmailContent += clientDataBodyResponse
    
    connectionSocket.send('250 Message accepted for delivery\r\n'.encode())

    quitResponse = connectionSocket.recv(1024).decode()
    if (quitResponse == 'QUIT\r\n'):
        connectionSocket.send('221 dummyserver.com closing connection\r\n'.encode())
    else:
        connectionSocket.send('quit not sent, closing connections anyways\r\n'.encode())

    connectionSocket.close()



