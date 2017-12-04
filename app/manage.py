from flask_script import Manager
from phonetree import app
from phonetree.db import init_db

manager = Manager(app)


@manager.command
def init():
    init_db()

if __name__ == '__main__':
    manager.run()
