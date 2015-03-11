import Server

def main():
    server = Server.Server()
    server.start()
    while server.running:
        pass

if __name__== "__main__":
    main()