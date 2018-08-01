from tcp_chat.server import Server


def start_server():
    server = Server()
    server.run()