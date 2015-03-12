import socket
import threading
import time

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
        responseSocket = socket.socket()
        responseSocket.connect(("localhost", 12346))

        request = None
        while request <> "QUI":
            request = raw_input("Enter your message > ")
            requestSocket.send(request)
            response = responseSocket.recv(1024)
            print "Request:{0}, Response:{1}".format(request, response)

        print "DONE!"
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