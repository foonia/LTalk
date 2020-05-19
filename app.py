from flask import Flask, request, render_template, redirect, url_for, session
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)


@app.route('/')
def index():
    return redirect('login')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/main')
def main():
    username = request.args.get('username')
    room = request.args.get('room')

    if username and room:
        return render_template('main.html')
    else:
        return redirect(url_for('index'))


@socketio.on('message')
def handle_message(msg):
    print('Message: {}'.format(msg))
    send(msg, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)
