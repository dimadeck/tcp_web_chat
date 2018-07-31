class Connected:
    def __init__(self):
        self.connections = []
        self.users = {}
        self.addrs = {}
        self.registered = []

    def add_connection(self, connection):
        self.connections.append(connection)

    def add_user(self, connection, username):
        self.users[connection] = username

    def add_addr(self, connection, addr):
        self.addrs[connection] = addr

    def is_valid_name(self, username):
        if username in self.users.values():
            return -1
        else:
            return 0

    def register_user(self, connection, username, addr):
        self.add_user(connection, username)
        self.add_addr(connection, addr)
        self.registered.append(connection)

    def is_register(self, connection):
        if connection in self.registered:
            return True
        else:
            return False

    def get_connection_by_username(self, username):
        for connection in self.connections:
            if username == self.users[connection]:
                return connection

    def get_name_by_connection(self, connection):
        try:
            return self.users[connection]
        except KeyError:
            return 0

    def get_addr_by_connection(self, connection):
        try:
            return self.addrs[connection]
        except KeyError:
            return 0

    def drop_connection(self, connection):
        if self.is_register(connection):
            self.users.pop(connection)
            self.addrs.pop(connection)
            self.registered.remove(connection)
        if connection in self.connections:
            self.connections.remove(connection)

    def get_user_list(self):
        user_list = []
        for username in self.users.values():
            user_list.append(username)
        return user_list

    def get_addr_list(self):
        addr_list = []
        for addr in self.addrs.values():
            addr_list.append(addr)
        return addr_list

    def get_registered(self):
        return self.registered

    def get_connections(self):
        return self.connections
