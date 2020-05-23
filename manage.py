import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_socketio import SocketIO

from app import create_app, db

app = create_app(os.getenv('FLASK_ENV') or 'dev')

# app.app_context().push()
manager = Manager(app)
# migrate = Migrate(app, db)
# manager.add_command('db', MigrateCommand)

socketio = SocketIO(app)

@manager.command
def run():
    socketio.run(app)

@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'],data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data)


if __name__ == '__main__':
    manager.run()
