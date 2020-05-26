from flask import (
    Blueprint, render_template, request, session,
    g, redirect, url_for, make_response
)

from flask_socketio import send, join_room, emit
import pymysql
from ..model.User import User
from app import socketio

general_bp = Blueprint('general_bp', __name__, template_folder='templates')

class MysqlClass:
    def __init__(self):
        self.conn = pymysql.connect(host="localhost", user="Acapellia", password="long503827!", db="ltalk")
        self.cur = self.conn.cursor()
        self.query = ''
mysql = MysqlClass()

''' 세션 용도에서 지금은 보류
@general_bp.before_request
def before_request():
    CUser = request.cookies.get('userid')
    if 'userid' in session:
        user = [x for x in users if x.id == session[userid]][0]
'''

@general_bp.route('/')
def index():
    return redirect('login')


@general_bp.route("/login", methods=['GET', 'POST'])
def login():
    resp = make_response(redirect(url_for('general_bp.chat')))
    if request.method == 'POST':
        session.pop('userid', None)
        userid = request.form['username']
        room = request.form['room']

        resp.set_cookie('userid',userid)
        resp.set_cookie('room',room)

        # db에서 확인하는 부분
        user = None
        mysql.query = "select * from user where id=%s"
        data = mysql.cur.execute(mysql.query, (userid))

        if (len(mysql.cur.fetchall()) > 0):
            user = User(id=userid, pw='', name='')
            print("Send LoginSuccess to client")
        else:
            print("Send LoginFail to client")
        
        '''#현재 pw가 없음
        if user and user.password == password:
            session[username] = user.username
            return redirect(url_for('profile'))
        '''

        if user and room:
            session['userid'] = user.id
            session['room'] = room
            return resp
        return redirect(url_for('general_bp.login'))

    return render_template('login.html')

''' # 현재 프로필 사용 x
@general_bp.route("/profile")
def profile():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('profile.html')
'''


@general_bp.route("/main")
def chat():
    userid = session.get('userid')
    room = session.get('room')
    if userid and room:
        return render_template('main.html', username=userid, room=room)

    '''
    userid = request.cookies.get('userid')
    room = request.args.get('room')
    room = request.cookies.get('room')
    '''

    if room:
        return render_template('main.html', username=userid, room=room)
    else:
        return redirect(url_for('general_bp.login'))

# broadcast 할 필요 없습니다. 혹시나해서 설정한거라
@socketio.on('joined', namespace='/chat')
def handle_join_room_event(data):
    userid = session.get('userid')
    room = session.get('room')

    join_room(room)

    emit('join_room_announcement', {'username': userid, 'room':room}, broadcast=True)
    #general_bp.logger.info("{} has joined the room {}".format(data['username'],data['room']))



@socketio.on('key_press', namespace='/chat')
def handle_key_event(data):
    room = session.get('room')
    print(data['keyCode'])
    emit("message", {'data':data, 'room' : room},broadcast=True)
    #general_bp.logger.info("key {}".format(data['keyCode']))

