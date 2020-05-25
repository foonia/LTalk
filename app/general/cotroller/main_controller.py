from flask import (
    Blueprint, render_template, request, session,
    g, redirect, url_for, make_response
)
from flask_socketio import send, join_room, emit

from ..model.User import User
from app import socketio

general_bp = Blueprint('general_bp', __name__, template_folder='templates')

###############################################################
users = []
users.append(User(id=1, username='Acapellia', password=''))
users.append(User(id=2, username='a', password=''))
users.append(User(id=3, username='b', password=''))
###############################################################


# @general_bp.before_request
# def before_request():
#     CUser = request.cookies.get('username')
#     if 'username' in session:
#         user = [x for x in users if x.id == session[CUser]][0]


@general_bp.route('/')
def index():
    return redirect('login')


@general_bp.route("/login", methods=['GET', 'POST'])
def login():
    # resp = make_response(redirect(url_for('general_bp.chat')))
    if request.method == 'POST':
        username = request.form['username']
        room = request.form['room']
        session['username'] = username
        session['room'] = room
        return redirect(url_for('general_bp.chat'))
        # resp.set_cookie('username', username)
        # resp.set_cookie('room', room)
        # user = [x for x in users if x.username == username][0]

        '''
        if user and user.password == password:
            session[username] = user.username
            return redirect(url_for('profile'))
        '''
        # if user and room:
        #     session[username] = user.username
        #     return resp
        # return redirect(url_for('general_bp.login'))

    return render_template('login.html')

'''
@general_bp.route("/profile")
def profile():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('profile.html')
'''


@general_bp.route("/main")
def chat():
    username = session.get('username')
    room = session.get('room')

    if username and room:
        return render_template('main.html', username=username, room=room)
    else:
        return redirect(url_for('general_bp.login'))

# broadcast 할 필요 없습니다. 혹시나해서 설정한거라
@socketio.on('joined', namespace='/chat')
def handle_join_room_event(data):
    username = session.get('username')
    room = session.get('room')

    join_room(room)
    emit('join_room_announcement', {'username': username, 'room':room}, broadcast=True)


@socketio.on('key_press', namespace='/chat')
def handle_key_event(data):
    room = session.get('room')
    print(data['keyCode'])
    emit("message", {'data':data, 'room' : room},broadcast=True)

