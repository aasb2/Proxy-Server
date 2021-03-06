from socket import *
#Biblioteca Necessária para criar threads
import threading
import time



#Função que encontra o endereço do host de uma requisição http
def findHost(request:str) -> str:
    length = len('Host: ')
    start = request.find('Host: ')
    if(start == -1):
        return None
    end = request.find('\r\n',start+length,len(request)-1)
    host = request[start+length:end]
    return host

#Função que retorna a versão do protocolo http em uma requisição
def findHTTP(request:str) -> str:
    length = len('HTTP/')
    start = request.find('HTTP/')
    end = request.find('\r\n')
    return request[start+length:end]

def requestWeb(connectionSocket = None, addr = None, thread = None):
    print("Starting Thread: ",thread)
    
    connection = True
    #Recebe requisição do cliente
    try:
        request = connectionSocket.recv(1024).decode()
        print("From Client: ",request)
        #encontra a versão HTTP
        version = findHTTP(request)
        #Encontra o host no request do cliente
        host = findHost(request)
        if host!= None:
            print(host)
            #Inicia conexão com o servidor web
            send_request_socket = socket(AF_INET, SOCK_STREAM)
            send_request_socket.connect((host,80)) 
            #Envia a primeira requisição ao servidor Web
            send_request_socket.send(request.encode())
            #Retorna a primeira página requisitada pelo cliente
            web_page = send_request_socket.recv(1024)
            connectionSocket.send(web_page)
        #Caso a versão http seja superior a 1.0 assume que é uma conexão persistente
        if version!= '1.0':
            while connection:
                #print(rq)
                try:
                    rq = connectionSocket.recv(1024)
                    #Caso a conexão com o cliente esteja encerrada, termina o loop
                    if rq == b'':
                        break
                    request = rq.decode()
                    #print("From Client: ",request)
                    #É necessário uma Exceção em caso de fechar o servidor web
                    send_request_socket.send(request.encode())
                    web_page = send_request_socket.recv(1024)
                    #Caso a conexão com o servidor web seja encerrada, termina o loop
                    if web_page == b'':
                        break
                    connectionSocket.send(web_page)
                except timeout as e:
                    print(e)
                    break
   #em caso de timeout trata a exceção
    except timeout as e:
        print("Connection ",e)
    finally:
        print("Closing Connection")
        send_request_socket.close()
        connectionSocket.close()
        print("Finishing Thread: ",thread)
    

#Determina a porta do servidor
serverPort = 13000
#Inicia a conexão socket do servidor criando uma conexão socket de boas vindas
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("The server is ready to receive")
th_num = 0

while True:
  #print("back to main")
  #Aceita conexão do client
  connectionSocket, addr = serverSocket.accept() 
  #inicia um timeout de 10 segundos, ou seja se o cliente não enviar nada em 10 segundos a conexão encerra
  connectionSocket.settimeout(10)
  #Cria uma thread e envia o socket da conexão com o cliente como argumento, para receber as requisições
  thread = threading.Thread(target = requestWeb, kwargs = dict(connectionSocket = connectionSocket, addr = addr, thread = th_num))
  print("creating thread: ", th_num)  
  th_num += 1
  #inicia a thread
  thread.start()




