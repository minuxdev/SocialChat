from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from werkzeug import debug
from time import strftime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'AKSJDFLAJDF'
socket = SocketIO(app)

users = {}
active_users = []
messages = []
chat_time = strftime("%Y-%m-%d %H:%M:%S")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat')
def chat_room():
    return render_template('chat.html')



@socket.on('entering')
def login_handler(json):
    user = json['user'].lower()
    if user not in active_users:
        users[user] = request.sid
        
        active_users.append(user)
    
    emit('user_added', active_users, broadcast=True)
    emit('historic', messages)


@socket.on('disconnect')
def leaving():
    for key, value in users.items():
        if request.sid == value:
            msg = f"{key}: left..."
            emit('leaving', msg, broadcast=True)
            users.pop(key)
            active_users.pop(key)
            break


@socket.on('chatting')
def chat_handler(msg):

    for key, value in users.items():
        if request.sid == value:
            message = f"{key}: {msg}"    
            emit('chatroom', message, broadcast=True)
        
    message = f"[{chat_time}]\n{key}: {msg}"
    messages.append(message)
    print(request.sid)
    


if __name__ == '__main__':
    socket.run(app, debug=True)