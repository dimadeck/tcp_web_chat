import socket


class Bind:

    def __init__(self):
        self.connections = {}

    def new_web_connection(self, key):
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sock.connect(("127.0.0.1", 10000))
        self.connections[key] = tcp_sock
        print(self.connections[key])

    def web_to_tcp(self, **kw):
        try:
            mode = kw['mode']
            key = kw['key']
            connect = self.connections[key]
        except KeyError:
            mode = -1
        msg = ''
        if mode in [0, 1, 2]:
            if mode == 0:
                msg = f'login {kw["name"]}'
            elif mode == 1:
                msg = f'msgall {kw["message"]}'
            elif mode == 2:
                msg = f'logout'
            connect.send(bytes(msg, 'utf-8'))

    def tcp_to_web(self):
        pass
