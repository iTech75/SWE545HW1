import threading
import socket

class ServerThread(threading.Thread):
    def __init__(self, clientSocket, clientAddress):
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress

    def run(self):
        while True:
            self.clientSocket.re

class Server(threading.Thread):
    """description of class"""
    def __init__(self):
        threading.Thread.__init__(self)
        self.socket = socket.socket()

    def run(self):
        self.socket.bind((socket.gethostname(), 12345))
        self.socket.listen(5)
        print("Server started")
        while True:
            clientSocket, clientAddress = self.socket.accept()

            print "Clint accepted"%clientAddress

        print("Server ended")

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
