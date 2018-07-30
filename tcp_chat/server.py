import socket
import threading

from connected import Connected
from data_parser import DataParser


class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, addr='127.0.0.1', port=10000):
        self.sock.bind((addr, port))
        self.sock.listen(5)
        self.connected = Connected()
        print('[+] Server start')

    def run(self):
        while True:
            client, addr = self.sock.accept()
            thread = threading.Thread(target=self.handler, args=(client, addr))
            thread.daemon = True
            thread.start()
            self.connected.add_connection(client)
            print(f'[+]{str(addr[0])}:{str(addr[1])} connected')

    def handler(self, connection, addr):
        while True:
            data = connection.recv(1024)
            req = DataParser(data)
            if req.status == 0:
                if req.cmd == 'login':
                    self.login(connection, req.parameter, addr)
                elif req.cmd == "debug":
                    self.debug_info()
                else:
                    if self.connected.is_register(connection):
                        if req.cmd == 'msg':
                            self.send_message(self.connected.get_name_by_connection(connection), req.parameter,
                                              req.body_with_name_to_bytes(
                                                  f'{self.connected.get_name_by_connection(connection)}(*)'))
                        elif req.cmd == 'msgall':
                            self.send_all(
                                req.body_with_name_to_bytes(self.connected.get_name_by_connection(connection)))
                        elif req.cmd == 'logout':
                            self.logout(connection)
                            break
                        else:
                            self.additional_commands(req.cmd, connection)

            else:
                connection.send(bytes(req.STATUS_DICT[req.status], 'utf-8'))
            if not data:
                self.logout(connection)
                break

    def additional_commands(self, cmd, connection):
        if cmd == 'whoami':
            connection.send(bytes(self.connected.get_name_by_connection(connection), 'utf-8'))
        elif cmd == 'userlist':
            connection.send(bytes(self.connected.get_user_list(), 'utf-8'))

    def login(self, connection, username, addr):
        if self.connected.register_user(connection, username, addr) == 0:
            print(
                f'[+]{str(addr[0])}:{str(addr[1])} log in at '
                f'{self.connected.get_name_by_connection(connection)}')
            self.send_all(bytes(f'[ServerMessage] - [{username}] log in.', "utf-8"))
        else:
            connection.send(bytes('[ServerMessage] - login failed.', 'utf-8'))

    def send_message(self, sender, username, message):
        for connection in self.connected.registered:
            if self.connected.users[connection] == username or self.connected.users[connection] == sender:
                connection.send(message)

    def send_all(self, message):
        for connection in self.connected.registered:
            connection.send(message)

    def logout(self, connection):
        username = self.connected.get_name_by_connection(connection)
        self.connected.drop_connection(connection)
        connection.close()
        print(f'[-]{username} disconnected')
        self.send_all(bytes(f'[ServerMessage] - [{username}] log out.', "utf-8"))

    def debug_info(self):
        print('###------[START DEBUG]------###')
        print(f'users: {self.connected.users.values()}')
        print(f'addrs: {self.connected.addrs.values()}')
        print(f'registered: {self.connected.registered}')
        print('###------[END DEBUG]------###')
