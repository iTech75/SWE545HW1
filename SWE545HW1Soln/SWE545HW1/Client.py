import socket
import threading
import time

class Client(threading.Thread):
    def __init__(self):
        super(Client, self).__init__()
        self.running = True

    def run(self):
        clientSocket = socket.socket()
        clientSocket.connect(("localhost", 12345))
        request = None
        while request <> "QUI":
            request = raw_input("Enter your message > ")
            clientSocket.send(request)
            response = clientSocket.recv(1024)
            print "Request:{0}, Response{1}".format(request, response)

        print "DONE!"
        raw_input()
        self.running = False

def main():
    client = Client()
    client.start()
    while client.running:
        time.sleep(1)
    print "Client closed!"

if __name__== "__main__":
    main()