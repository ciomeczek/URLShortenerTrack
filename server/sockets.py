from server import socketio
from flask_socketio import emit
from flask_socketio import join_room


@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)


@socketio.on('message')
def handle_message(data):
    emit('message', data, to=data['room'])
