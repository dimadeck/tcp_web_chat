from flask import session
from flask_socketio import emit, join_room, leave_room

from web_chat import socketio_chat, room, bind


@socketio_chat.on('open', namespace='')
def open(message):
    try:
        key = session['csrf_token']
        bind.new_web_connection(key)
        bind.launch()
    except:
        pass


@socketio_chat.on('joined', namespace='/chat')
def joined(message):
    name = session.get("name")
    msg = f'{name} has entered.'
    join_room(room)
    emit('status', {'msg': msg}, room=room)
    key = session['csrf_token']
    bind.web_to_tcp(mode=0, name=name, key=key)
    print(msg)


@socketio_chat.on('text', namespace='/chat')
def text(message):
    name = session.get("name")
    msg = message["msg"]
    emit('message', {'msg': f'{name}: {msg}'}, room=room)
    key = session['csrf_token']
    bind.web_to_tcp(mode=1, name=name, message=msg, key=key)


@socketio_chat.on('left', namespace='/chat')
def left(message):
    name = session.get("name")
    msg = f'{name} has left.'
    leave_room(room)
    emit('status', {'msg': msg}, room=room)
    key = session['csrf_token']
    bind.web_to_tcp(mode=2, name=name, key=key)
    print(msg)
