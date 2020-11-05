# Import socket module
# Import sys to terminate the program
from socket import *
import os


def server():
    serverPort = 12344 # fixed arbitrary port number
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(('',serverPort))      
    serverSocket.listen(1) 
    print("The server host and port are: ", serverSocket.getsockname())
    print("The server is ready to receive . .")

    while True:
    
        connectionSocket, addr = serverSocket.accept() 
        print("Request accepted from: %s" % (addr,))

        try:
            # Recieve message and check file name
            message = connectionSocket.recv(1024).decode()
            if (message.split()[2] == 'HTTP/1.1'):
                if (message.split()[0] == 'GET'):
                    filename = message.split()[1]
                    if filename.split(".")[1] == "html":
                        f = open("./"+filename[1:], 'r')
                    else:
                        f = open("./"+filename[1:], 'rb')                    
                    message2return = f.read()

                    print("File found.")
                    # Returns header line informing that the file was found
                    headerLine = "HTTP/1.1 200 OK\r\n"
                    connectionSocket.send(headerLine.encode())
                    connectionSocket.send("\r\n".encode())
                    sizeOfFile = f.seek(0, os.SEEK_END)
                    connectionSocket.send(("The size of the file requested is: " + str(sizeOfFile)+ " bytes.").encode())
                    connectionSocket.send("\r\n".encode()) 
                    
                    checkfiletype(filename.split(".")[1], connectionSocket)               
                    
                    connectionSocket.send("\r\n".encode())

                    # Sends the file
                    if filename.split(".")[1] == "html":
                        for i in range(len(message2return)):
                            connectionSocket.send(message2return[i].encode())
                        connectionSocket.send("\r\n".encode())
                    else:
                        for i in range(len(message2return)):
                            connectionSocket.send(repr(message2return[i]).encode('utf-8'))
                        connectionSocket.send("\r\n".encode())
                    # Terminates the conection
                    print("File sent.")
                    connectionSocket.close()
                else:
                    ERR501(connectionSocket)
            else:
                ERR505(connectionSocket)

        except IOError:
            ERR404(connectionSocket)

def ERR404(connectionSocket):
    print("Warning: file not found.\r\n")
    Header = "HTTP/1.1 404 Not Found\r\n"
    connectionSocket.send(Header.encode())
    connectionSocket.send("\r\n".encode())
    mess = "The requested URL was not found on this server.\r\n"
    connectionSocket.send(mess.encode())
    connectionSocket.send("\r\n".encode())
    connectionSocket.close()
    
def ERR505(connectionSocket):
    print("HTTP version not supported.\r\n")
    Header = "HTTP/1.1 505 Version Not Supported\r\n"
    connectionSocket.send(Header.encode())
    connectionSocket.send("\r\n".encode())
    mess = "This web server only supports HTTP/1.1.\r\n"
    connectionSocket.send(mess.encode())            
    connectionSocket.send("\r\n".encode())
    connectionSocket.close()


def ERR501(connectionSocket):
    Header = "HTTP/1.1 501 Method Not Implemented\r\n "
    connectionSocket.send(Header.encode())
    connectionSocket.send("\r\n".encode())
    mess = "Invalid method in request.\r\n"
    connectionSocket.send(mess.encode())
    connectionSocket.send("\r\n".encode())
    connectionSocket.close()


def checkfiletype(filetype, connectionSocket):
    if filetype == "gif":
        connectionSocket.send("The type of file requested is: gif ".encode())
    elif filetype == "jpg":
        connectionSocket.send("The type of file requested is: jpg ".encode())
    elif filetype == "jpeg": 
        connectionSocket.send("The type of file requested is: jpeg ".encode())
    elif filetype == "html":#do nothing if file type is html
        connectionSocket.send("\r\n".encode())       

if __name__ == "__main__":
    server()