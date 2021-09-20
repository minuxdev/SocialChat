from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from werkzeug import debug


app = Flask(__name__)
app.config['SECRET_KEY'] = 'AKSJDFLAJDF'
socket = SocketIO(app)

users = {}
messages = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat')
def chat_room():
    return render_template('chat.html')





@socket.on('entering')
def login_handler(json):
    user = json['user'].lower()
    users[user] = request.sid
    
    emit('user_added', f'{user.title()}: is online...', broadcast=True)

@socket.on('disconnect')
def leaving():
    print(users)
    for key, value in users.items():
        if request.sid == value:
            msg = f"{key}: left..."
            emit('leaving', msg, broadcast=True)
            users.pop(key)
            print(users)
            break


@socket.on('from chat')    
def welcome_handler(msg):
    print(msg)
    emit('start_chat', 'Welcome in...')
    

@socket.on('chatting')
def chat_handler(msg):

    for key, value in users.items():
        if request.sid == value:
            message = f"{key}: {msg}"
            
    emit('chatroom', message, broadcast=True)
    


if __name__ == '__main__':
    socket.run(app, debug=True)