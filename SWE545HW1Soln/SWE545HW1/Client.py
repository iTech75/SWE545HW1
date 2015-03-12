import socket
import threading
import time

class ClientResponseHandler(threading.Thread):
    def __init__(self):
        super(ClientResponseHandler, self).__init__()
        self.running = True

    def run(self):
        responseSocket = socket.socket()
        responseSocket.connect(("localhost", 12346))
        while self.running:
            response = responseSocket.recv(1024)
            if response[:3] == "TIM":
                responseSocket.send("Peki")
                print "Time received: " + response[3:]
            else:
                print "Response:{0}".format(response)
        responseSocket.close()
                
class Client(threading.Thread):
    """
    Client

    Client class, talks with Server class over 2 sockets:12345 for request sending,
    12346 for incoming responses for the requests
    """
    def __init__(self):
        super(Client, self).__init__()
        self.running = True

    def run(self):
        requestSocket = socket.socket()
        requestSocket.connect(("localhost", 12345))
        responseHandler = ClientResponseHandler()
        responseHandler.start()

        request = None
        print "You can enter your messages to server, when the response arrives, you will be notified!"
        while request <> "QUI":
            request = raw_input()
            requestSocket.send(request)

        requestSocket.close()
        print "DONE!"
        responseHandler.running = False
        raw_input()
        self.running = False

def main():
    """
    main

    Entry point for client...
    """
    client = Client()
    client.start()
    while client.running:
        time.sleep(1)
    print "Client closed!"

if __name__== "__main__":
    main()