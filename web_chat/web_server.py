from web_chat import socketio_chat, create_app, bind


def start_server():
    try:
        app = create_app(False)
        socketio_chat.run(app)
    except KeyboardInterrupt:
        exit(0)
