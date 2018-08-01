from web_chat import socketio_chat, create_app


def start_server():
    app = create_app()
    socketio_chat.run(app)
