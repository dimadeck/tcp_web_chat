import sys

from tcp_chat.client import Client
from tcp_chat.server import Server

if __name__ == '__main__':
    if len(sys.argv) > 1:
        client = Client(sys.argv[1])
    else:
        try:
            server = Server()
            server.run()
        except KeyboardInterrupt:
            exit(0)
