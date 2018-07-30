import socket
import threading


class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_msg(self):
        while True:
            self.sock.send(bytes(input(""), 'utf-8'))

    def __init__(self, address):
        self.sock.connect((address, 10000))
        thread = threading.Thread(target=self.send_msg)
        thread.daemon = True
        thread.start()

        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            print(str(data, 'utf-8'))
