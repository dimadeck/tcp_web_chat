import socket


class Bind:
    def __init__(self):
        pass

    def connect_to_tcp(self):
        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_sock.connect(("127.0.0.1", 10000))

    def web_to_tcp(self, **kw):
        mode = kw['mode']
        msg = ''
        if mode in [0,1,2]:
            if mode == 0:
                msg = f'login {kw["name"]}'
            elif mode == 1:
                msg = f'msgall {kw["message"]}'
            elif mode == 2:
                msg = f'logout'
            self.tcp_sock.send(bytes(msg, 'utf-8'))

    def tcp_to_web(self):
        pass
