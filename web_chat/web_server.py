from flask import Blueprint
from flask import Flask
from flask import redirect, url_for, render_template, request
from flask import session
from flask_socketio import SocketIO
from flask_socketio import emit, join_room, leave_room
from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired

main_chat = Blueprint('main', __name__, template_folder='templates')
socketio_chat = SocketIO()


@socketio_chat.on('joined', namespace='/chat')
def joined(message):
    room = 'Chat'
    join_room(room)
    emit('status', {'msg': f'{session.get("name")} has entered.'}, room=room)


@socketio_chat.on('text', namespace='/chat')
def text(message):
    room = 'Chat'
    emit('message', {'msg': f'{session.get("name")}: {message["msg"]}'}, room=room)


@socketio_chat.on('left', namespace='/chat')
def left(message):
    room = 'Chat'
    leave_room(room)
    emit('status', {'msg': f'{session.get("name")} has left the room.'}, room=room)


class LoginForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Enter to chat')


@main_chat.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('.chat'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
    return render_template('index.html', form=form)


@main_chat.route('/chat')
def chat():
    name = session.get('name', '')
    if name == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name)


def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
    app.register_blueprint(main_chat)
    socketio_chat.init_app(app)
    return app


def start_server():
    app = create_app(debug=True)
    socketio_chat.run(app)
