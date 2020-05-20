from flask import (
    Blueprint, render_template, request, session,
    g, redirect, url_for
)
from flask_socketio import send, join_room

from ..model.User import User


main = Blueprint('main', __name__, template_folder='templates')

###############################################################
def init_data():
    users = []
    users.append(User(id=1, username='Acapellia',password=''))
    users.append(User(id=2, username='a',password=''))
    users.append(User(id=3, username='b',password=''))
###############################################################


@main.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user


@main.route('/')
def index():
    return redirect('login')


@main.route("/login", methods=['GET', 'POST'])
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


@main.route("/profile")
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')


@main.route("/insertroom")
def chat():
    username = 'guest'
    room = request.args.get('room')
    if room:
        return render_template('main.html', username=username, room=room)
    else:
        return redirect(url_for('login'))

