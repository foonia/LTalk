from flask import (
    Flask, request, render_template, redirect, url_for, session, g
)
from flask_socketio import SocketIO, send, join_room

class User:
    def __init__(self,id,username,password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='Acapellia',password=''))
users.append(User(id=2, username='a',password=''))
users.append(User(id=3, username='b',password=''))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

@app.route('/')
def index():
    return redirect('login')


@app.route("/login", methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']

        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('main'))
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/main/')
def main():
    user = session['user_id']
    if not g.user:
        return redirect(url_for('login'))

    return render_template('ltalk.html')

@app.route('/chat')
def chat():
    username = session['user_id']
    print(username)
    room = request.args.get('room')
    if username and room:
        return render_template('ChatMain.html',username=username,room=room)
    else:
        return redirect(url_for('index'))

@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has sent message to the room {}".format(
        data['username'], data['room'], data['message']
    ))
    socketio.emit('receive_message',data,room=data['room'])

@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'],data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data)

@socketio.on('message')
def handle_message(msg):
    print('Message: {}'.format(msg))
    send(msg, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)
