from flask import session
from flask_socketio import emit, join_room, leave_room
from web_chat import socketio_chat, room


@socketio_chat.on('joined', namespace='/chat')
def joined(message):
    msg = f'{session.get("name")} has entered.'
    join_room(room)
    emit('status', {'msg': msg}, room=room)
    print(msg)


@socketio_chat.on('text', namespace='/chat')
def text(message):
    emit('message', {'msg': f'{session.get("name")}: {message["msg"]}'}, room=room)


@socketio_chat.on('left', namespace='/chat')
def left(message):
    msg = f'{session.get("name")} has left.'
    leave_room(room)
    emit('status', {'msg': msg}, room=room)
    print(msg)
