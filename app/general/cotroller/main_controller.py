from flask import (
    Blueprint, render_template, request, session,
    g, redirect, url_for
)
from flask_socketio import send, join_room

from ..model.User import User
from app import socketio

general_bp = Blueprint('general_bp', __name__)

###############################################################
users = []
users.append(User(id=1, username='Acapellia', password=''))
users.append(User(id=2, username='a', password=''))
users.append(User(id=3, username='b', password=''))
###############################################################


@general_bp.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user


@general_bp.route('/')
def index():
    return redirect('login')


@general_bp.route("/login", methods=['GET', 'POST'])
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


@general_bp.route("/profile")
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')


@general_bp.route("/insertroom")
def chat():
    username = 'guest'
    room = request.args.get('room')
    if room:
        return render_template('main.html', username=username, room=room)
    else:
        return redirect(url_for('login'))


@socketio.on('join_room')
def handle_join_room_event(data):
    # app.logger.info("{} has joined the room {}".format(data['username'],data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data)

