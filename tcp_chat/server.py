import socket
import threading

from tcp_chat.connected import Connected
from tcp_chat.data_parser import DataParser
from tcp_chat.http_parser import HttpParser


class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, addr='0.0.0.0', port=10000):
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
            client = self.who_is_client(data)
            if client == 1:
                pass
                # http = HttpParser(data)
                # ws = WebSide(http)
                # ws.run_http(connection, http.req_dict)
            elif client == 2:
                req = DataParser(data)
                if req.status == 0:
                    if self.run_command(connection, req, addr) == -1:
                        break
                else:
                    connection.send(bytes(req.STATUS_DICT[req.status], 'utf-8'))
            if not data:
                self.logout(connection)
                break

    @staticmethod
    def who_is_client(data, encoding='utf-8', separator=' '):
        cmd = data.decode(encoding).split(separator)[0]
        if cmd in HttpParser.ALLOWED_METHOD:
            return 1
        else:  # elif cmd in DataParser.CMD_LIST:
            return 2
        # Обработка ошибок реализована на уровне DataParser

    def run_command(self, connection, req, addr):
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
                    return -1
                else:
                    self.additional_commands(req.cmd, connection)
            else:
                connection.send(bytes('Please log in!', "utf-8"))
        return 0

    def additional_commands(self, cmd, connection):
        if cmd == 'whoami':
            connection.send(bytes(self.connected.get_name_by_connection(connection), 'utf-8'))
        elif cmd == 'userlist':
            user_list = self.connected.get_user_list()
            connection.send(bytes(','.join(user_list), 'utf-8'))

    def login(self, connection, username, addr):
        if self.connected.is_valid_name(username) == 0:
            self.connected.register_user(connection, username, addr)
            print(
                f'[+]{str(addr[0])}:{str(addr[1])} log in at ['
                f'{self.connected.get_name_by_connection(connection)}]')
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
        print(f'[-][{username}] disconnected')
        self.send_all(bytes(f'[ServerMessage] - [{username}] log out.', "utf-8"))

    def debug_info(self):
        print('###------[START DEBUG]------###')
        print(f'users: {self.connected.users.values()}')
        print(f'addrs: {self.connected.addrs.values()}')
        print(f'registered: {self.connected.registered}')
        print('###------[END DEBUG]------###')

    @staticmethod
    def debug_request(data):
        print('###------[START REQUEST DEBUG]------###')
        print(f'{data}')
        print('###------[END REQUEST DEBUG]------###')
