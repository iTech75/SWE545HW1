import threading
import socket
import Queue
import datetime

class ResponseSender(threading.thread):
    def __init__(self, queue, responseSocket):
        super(ResponseSender, self).__init__()
        assert isinstance(queue, Queue.Queue)
        assert isinstance(responseSocket, socket.socket)

        self.running = True
        self.queue = queue
        self.responseSocket = responseSocket

    def run(self):
        
        while self.running:
            response = self.queue.get()
            self.responseSocket.send(response)

class RequestHandler(threading.Thread):
    def __init__(self, clientSocket, clientAddress):
        super(RequestHandler, self).__init__()
        assert isinstance(clientSocket, socket.socket)
        assert isinstance(clientAddress, tuple)

        self.clientSocket = clientSocket
        self.clientAddress = clientAddress

    def run(self):
        while True:
            request = self.clientSocket.recv(1024)
            response = self.parser(request)
            self.clientSocket.send(response)

    def parser(self, request):
        strippedrequest = request.strip()

        if strippedrequest is None:
            response = "ERR"
        elif strippedrequest[0:3] == "HEL":
            response = "SLT"
        elif strippedrequest[0:3] == "TIC":
            response = "TOC " + datetime.datetime.now().strftime("%d/%m/%Y, %H:%M")
        elif strippedrequest[0:3] == "GET":
            key = strippedrequest[4:]
            if key in self.__definitions:
                response = "CDE " + self.__definitions[key]
            else:
                response = "NTF " + key
        elif strippedrequest[0:3] == "QUI":
            response = "BYE"
        else:
            response = "ERR"

        return response
            

class Server(threading.Thread):
    """description of class"""
    def __init__(self):
        super(Server, self).__init__()
        self.running = True

    def run(self):
        serverSocket = socket.socket()
        serverSocket.bind(("", 12345))
        serverSocket.listen(5)
        print("Server started")
        while self.running:
            clientSocket, clientAddress = serverSocket.accept()
            print "Clint accepted {0}".format(clientAddress)
            handler = RequestHandler(clientSocket, clientAddress)
            handler.start()

        print("Server ended")

def main():
    server = Server()
    server.start()
    while server.running:
        pass

if __name__== "__main__":
    main()