import sys

from tcp_chat.client import Client
from tcp_chat.tcp_server import start_server as tcp_start
from web_chat.web_server import start_server as ws_start

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if 'web' in sys.argv:
            ws_start()
        else:
            client = Client(sys.argv[1])
    else:
        tcp_start()
