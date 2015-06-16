import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask.ext.script import Manager, Server
from aggtron import app

from auth import auth_flask_login
from main_site import main_site_index
from api_auth import add_project

app.register_blueprint(auth_flask_login)
app.register_blueprint(main_site_index)
app.register_blueprint(add_project)

manager = Manager(app)

manager.add_command('runserver', Server(
                    use_debugger= True,
                    use_reloader = True,
                    host = '0.0.0.0'
                    )
)


if __name__ == '__main__':
    manager.run()