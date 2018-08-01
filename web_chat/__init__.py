from flask import Blueprint, Flask
from flask_socketio import SocketIO

room = 'Chat'
main_chat = Blueprint('main', __name__)
socketio_chat = SocketIO()

from web_chat import route, form, events


def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
    app.register_blueprint(main_chat)
    socketio_chat.init_app(app)
    return app
