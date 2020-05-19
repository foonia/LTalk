from flask import (
    Flask, render_template, request, session,
    g, redirect, url_for
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
            return redirect(url_for('profile'))
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route("/profile")
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')

@app.route("/insertroom")
def chat():
    username = 'guest'
    room = request.args.get('room')
    if room:
        return render_template('main.html',username=username,room=room)
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    socketio.run(app, debug=True)

