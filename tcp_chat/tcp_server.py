from tcp_chat.server import Server


def start_server():
    try:
        server = Server()
        server.run()
    except KeyboardInterrupt:
        exit(0)

