import socket
import threading


class Bind:

    def __init__(self):
        self.connections = {}
        self.not_launch = True

    def new_web_connection(self, key, addr="127.0.0.1"):
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sock.connect((addr, 10000))
        self.connections[key] = tcp_sock

    def web_to_tcp(self, **kw):
        try:
            mode = kw['mode']
            key = kw['key']
            connect = self.connections[key]
        except KeyError:
            mode = -1
        msg = ''
        if mode == 1 and kw["message"] == 'debug':
            self.tcp_to_web()
        else:
            if mode in [0, 1, 2]:
                if mode == 0:
                    msg = f'login {kw["name"]}'
                elif mode == 1:
                    msg = f'msgall {kw["message"]}'
                elif mode == 2:
                    msg = f'logout'
                connect.send(bytes(msg, 'utf-8'))

    def launch(self):
        if self.not_launch:
            thread = threading.Thread(target=self.tcp_to_web)
            thread.daemon = True
            thread.start()
            self.not_launch = False

    def tcp_to_web(self):
        while True:
            try:
                for key, connection in self.connections.items():
                    data = connection.recv(1024)
                    if not data:
                        self.connections.pop(connection)
                    print(str(data, 'utf-8'))
                if len(self.connections) == 0:
                    self.not_launch = True
                    break
            except RuntimeError:
                pass
