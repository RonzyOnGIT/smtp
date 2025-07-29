# checks to see if client sent a QUIT message to close connection
def check_for_quit(clientResponse, connectionSocket):
    if clientResponse == 'QUIT\r\n':
        connectionSocket.send('221 dummyserver.com closing connection\r\n'.encode())
        connectionSocket.close()
        return True
    return False
