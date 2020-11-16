from socket import *
#Bibliotecas Necessárias para criar threads
#import logging
import threading
import time


'''
def thread(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thead %s: finishing", name)
    print("It is me thread: ",i)



threads = []
for i in range(100):
    x = threading.Thread(target = thread, args = (i,))
    threads.append(x)
    x.start()
'''




def findHost(request:str) -> str:
    length = len('Host: ')
    start = request.find('Host: ')
    if(start == -1):
        return '-1'
    end = request.find('\r\n',start+length,len(request)-1)
    host = request[start+length:end]
    return host

def findHTTP(request:str) -> str:
    length = len('HTTP/')
    start = request.find('HTTP/')
    end = request.find('\r\n')
    return request[start+length:end]

def requestWeb(connectionSocket = None, addr = None, thread = None):
    print("Starting Thread: ",thread)
    rq = connectionSocket.recv(1024)
    #print(rq)
    while rq != b'':
        #print(rq)
        request = rq.decode()
        print("From Client: ",request)
        host = findHost(request)
        version = findHTTP(request)
        send_request_socket = socket(AF_INET, SOCK_STREAM)
        send_request_socket.connect((host,80))     
        send_request_socket.send(request.encode())
        web_page = send_request_socket.recv(1024)
        print("From Web Server: ", web_page.decode())
        connectionSocket.send(web_page)
        rq = connectionSocket.recv(1024)
    connectionSocket.close()
    print("Closing Thread: ",thread)
    


serverPort = 13000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("The server is ready to receive")
th_num = 0

while True:
  connectionSocket, addr = serverSocket.accept() 
  print("creating thread: ", th_num)
  thread = threading.Thread(target = requestWeb, kwargs = dict(connectionSocket = connectionSocket, addr = addr, thread = th_num))
  th_num += 1
  thread.start()




