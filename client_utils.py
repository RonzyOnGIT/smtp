# prompts the client to quit or not 
def prompt_for_quit(clientSocket):
    quit = input('close connection? 0. No  1. Yes: ')
    print('\n')
    if quit == '1':
        clientSocket.send('QUIT\r\n'.encode())
        serverResponse = clientSocket.recv(1024).decode()
        if (serverResponse[:3] == '221'):
            print(serverResponse)
            clientSocket.close()
            return True
        else:
            print('Server did not acknowledge quit message, continuing on\n')
            return False
    else:  
        return False