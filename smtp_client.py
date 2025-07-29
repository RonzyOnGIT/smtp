from socket import *
from client_utils import prompt_for_quit
import sys


msg = "I love computer networks!\r\n" 
endmsg = ".\r\n" 

mailserver = input('Enter server IP: ')
mailPort = 1025

clientName = input('Enter client name: ')
clientEmail = input('Enter client email: ')

print('\n')

# create client socket
clientSocket = socket(AF_INET, SOCK_STREAM)

# establish TCP connection with specified mail server
clientSocket.connect((mailserver, mailPort))   

# initial server response after establishing TCP connection
recv = clientSocket.recv(1024).decode() 
print(recv) 

if recv[:3] != '220': 
    print('220 reply not received from server.') 
    clientSocket.close()
    sys.exit()

if prompt_for_quit(clientSocket):
    sys.exit()

heloCommand = 'HELO ' + clientName + '\r\n'
clientSocket.send(heloCommand.encode())

heloCommandResponse = clientSocket.recv(1024).decode()

print(heloCommandResponse)

if (heloCommandResponse[:3] != '250'):
    print('250 reply not received from server.')
    clientSocket.close()
    sys.exit()

if prompt_for_quit(clientSocket):
    sys.exit()

mailCommand = 'MAIL FROM: ' + '<'+ clientEmail + '>\r\n'
clientSocket.send(mailCommand.encode())

mailCommandResponse = clientSocket.recv(1024).decode()

print(mailCommandResponse)

if (mailCommandResponse[:3] != '250'):
    print("was not able to verify client")
    clientSocket.close()
    sys.exit()

if prompt_for_quit(clientSocket):
    sys.exit()

rcptMessage = 'RCPT TO: ' + '<bob@dummyserver.com>\r\n'
clientSocket.send(rcptMessage.encode())

rcptMessageResponse = clientSocket.recv(1024).decode()

print(rcptMessageResponse)

if (rcptMessageResponse[:3] != '250'):
    print('was not able to find recipient')
    clientSocket.close()
    sys.exit()

if prompt_for_quit(clientSocket):
    sys.exit()

dataMessage = "DATA\r\n"
clientSocket.send(dataMessage.encode())

dataMessageResponse = clientSocket.recv(1024).decode()

if (dataMessageResponse[:3] != "354"):
    print('Server did not response with 354 for body')
    clientSocket.close()
    sys.exit()

# add header stuff like subject in future
clientSocket.send(msg.encode())
clientSocket.send(endmsg.encode())

recv4 = clientSocket.recv(1024).decode()

if (recv4[:3] != '250'):
    print('message not accepted for delivery by server')
    clientSocket.close()
    sys.exit()

quitMessage = 'QUIT\r\n'
clientSocket.send(quitMessage.encode())

quitMessageResponse = clientSocket.recv(1024).decode()

if (quitMessageResponse[:3] != '221'):
    print('server did not send 221 response for quit')
    clientSocket.close()
    sys.exit()

print('successful smtp interaction!')
clientSocket.close()

