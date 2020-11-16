from socket import *
import time
serverName = "127.0.0.1"
serverPort = 13000 #12000
#http://data.pr4e.org
site1 = 'GET /romeo.txt HTTP/1.0\r\nHost: data.pr4e.org\r\n\r\n'
site2 = 'GET /~ross/ HTTP/1.1\r\nHost: cis.poly.edu\r\n\r\n'

#sentence = '' #input("Input lowercase sentence")

#while True:
time.sleep(5)
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
clientSocket.send(site1.encode())
modifiedSentence = clientSocket.recv(1024)
print("From Server: ",modifiedSentence.decode())
#clientSocket.close()
time.sleep(7)
clientSocket.send(site2.encode())
modifiedSentence = clientSocket.recv(1024)
print("From Server: ",modifiedSentence.decode())

clientSocket.send(site1.encode())
modifiedSentence = clientSocket.recv(1024)
print("From Server: ",modifiedSentence.decode())
clientSocket.close()
