import threading
import socket
import Queue
import datetime
import random

class ResponseSender(threading.Thread):
    """
    ResponseHandler

    Listens queue and send responses over the socket.

    Sometimes, before sending response, also sends time to the client.
    """
    def __init__(self, queue):
        super(ResponseSender, self).__init__()
        assert isinstance(queue, Queue.Queue)

        self.running = True
        self.queue = queue

    def run(self):
        
        while self.running:
            nextItem = self.queue.get()
            clientSocket = nextItem[0]
            response = nextItem[1]
            if random.randint(0, 1) == 1:
                clientSocket.send("TIM" + datetime.datetime.now().isoformat(" "))
                timeResponse = clientSocket.recv(1024)
                if timeResponse != "Peki":
                    print "Error in time response, should be 'Peki'"

            clientSocket.send(response)

    def EnqueueNewResponseToBeSend(self, targetSocket, response):
        self.queue.put((targetSocket, response))

class RequestHandler(threading.Thread):
    """
    RequestHandler

    Parses the requests coming from client then enqueues the responses to be send back to the client.
    """
    def __init__(self, clientSocket, clientAddress, clientResponseSocket, responseSender):
        super(RequestHandler, self).__init__()
        assert isinstance(clientSocket, socket.socket)
        assert isinstance(clientAddress, tuple)
        assert isinstance(clientResponseSocket, socket.socket)
        assert isinstance(responseSender, ResponseSender)

        self.clientSocket = clientSocket
        self.clientAddress = clientAddress
        self.clientResponseSocket = clientResponseSocket
        self.responseSender = responseSender

    def run(self):
        while True:
            request = self.clientSocket.recv(1024)
            response = self.parser(request)
            self.responseSender.EnqueueNewResponseToBeSend(self.clientResponseSocket, response)

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
    """
    Server

    Server object, initiates the environment and sockets.
    """
    def __init__(self):
        super(Server, self).__init__()
        self.running = True

    def run(self):
        queue = Queue.Queue()
        responseSender = ResponseSender(queue)
        responseSender.start()

        serverSocket = socket.socket()
        responseSocket = socket.socket()

        serverSocket.bind(("", 12345))
        responseSocket.bind(("", 12346))
        serverSocket.listen(5)
        responseSocket.listen(5)
        print("Server started")

        while self.running:
            clientSocket, clientAddress = serverSocket.accept()
            print "Clint accepted {0}".format(clientAddress)

            clientResponseSocket, clientResponseAddress = responseSocket.accept()
            print "Response connection established from: {0}".format(clientResponseAddress)
            handler = RequestHandler(clientSocket, clientAddress, clientResponseSocket, responseSender)
            handler.start()

        print("Server ended")

def main():
    """
    main

    entry point for server
    """
    server = Server()
    server.start()
    while server.running:
        pass

if __name__== "__main__":
    main()