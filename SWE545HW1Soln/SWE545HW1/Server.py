import threading
import socket

class Server(threading.Thread):
    """description of class"""
    def __init__(self):
        threading.Thread.__init__(self)
        self.socket = socket.socket()

    def run(self):
        self.socket.bind(self.socket.
        print("Server started")
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
