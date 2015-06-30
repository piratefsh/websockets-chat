from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

clients = []


@app.route('/')
def index():
    return "I'm live!"


@socketio.on('echo', namespace='/echo')
def echo(message):
    emit('response', {'data': 'echo: ' + message['data']})


@socketio.on('message', namespace='/echo')
def message(message):
    data = message['data']
    print('%s said %s' % (data['user'], data['text']))
    emit('response', {
         'data': {'user': data['user'], 'text': data['text']}}, broadcast=True)


@socketio.on('join', namespace='/echo')
def join(message):
    clients.append(message['data'])
    emit('joined', {'data': '%s is online' % message['data']}, broadcast=True)


@socketio.on('connect', namespace='/echo')
def connect():
    emit('connect', {'data': 'Connected', 'users': clients})


@socketio.on('disconnect', namespace='/echo')
def disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)
