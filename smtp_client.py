from socket import *

import sys


msg = "\r\n I love computer networks!" 
endmsg = "\r\n.\r\n" 

mailserver = ""
mailPort = 1025

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

heloCommand = 'HELO client\r\n'
clientSocket.send(heloCommand.encode())

recv1 = clientSocket.recv(1024).encode()
print(recv1)
if (recv1[:3] != '250'):
    print('250 reply not received from server.')
    sys.exit()

mailCommand = "MAIL FROM: nick@gmail.com"
clientSocket.send(mailCommand.encode())

recv2 = clientSocket.recv(1024).encode()
print(recv2)
if (recv2[:3] != '250'):
    print("was not able to verify client")
    sys.exit()

rcptMessage = 'RCPT TO: ' + 'bob@dummyserver.com'

recv3 = clientSocket.recv(1024).encode()
print(recv3)
if (recv3[:3] != '250'):
    sys.exit()

dataMessage = "DATA"


# # Send DATA command and print server response.  
# # Fill in start 
# # Fill in end 
# # Send message data. 
# # Fill in start 
# # Fill in end 
# # Message ends with a single period. 
# # Fill in start 
# # Fill in end 
# # Send QUIT command and get server response. 
# # Fill in start 
# # Fill in end 