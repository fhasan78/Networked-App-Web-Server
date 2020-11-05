
# Import socket module

from socket import *
import sys


def client(serverHost, serverPort, filename):
    # Create the TCP socket using the command line options given

    clientSocket = socket(AF_INET, SOCK_STREAM)

    try:
        clientSocket.connect((serverHost, int(serverPort)))
        print("Connection OK.")

        # Sending the HTTP request
        httpRequest = "GET /" + filename + " HTTP/1.1\r\n Host:" + serverHost + "\r\n"
        clientSocket.send(httpRequest.encode())

        # Recieving the response from the server
        print("From Server: \r\n")

        # Looping to make sure the whole message gets recieved
        messageRecv = ""
        while True:
            clientSocket.settimeout(5)
            m = clientSocket.recv(1024).decode('utf8')
            messageRecv += m
            if (len(m) == 0):
                break

        
        if messageRecv.split("\r\n")[0] == "HTTP/1.1 200 OK":
            print(messageRecv.split("\r\n",5)[0])
            print(messageRecv.split("\r\n",5)[1])
            print(messageRecv.split("\r\n",5)[2])
            print(messageRecv.split("\r\n",5)[3])
            savefile(messageRecv)
            print(messageRecv.split("\r\n",5)[5])
            

        else:
            print(messageRecv) # print the message recieved
        
        # Closing socket and ending the program
        print("Closing socket . .")
        clientSocket.close()
    except Exception as e: # In case the server is not available
        print("Connection refused.")
        print(e)
        clientSocket.close()
        

def savefile(messageRecv):
    # if the file requested is found have it saved in a file        
    with open("./"+filename, 'w') as f:
        f.write(messageRecv.split("\r\n",5)[5])
    

        
if __name__ == "__main__":

    if (len(sys.argv) != 4):
        print("Use: Client.py <server_host> <server_port> <filename>")
        sys.exit()
    else:
        serverHost, serverPort, filename = sys.argv[1:]
        client(serverHost, serverPort, filename)