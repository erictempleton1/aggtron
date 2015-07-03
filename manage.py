import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask.ext.script import Manager, Server
from aggtron import app

from auth import auth_flask_login
from main_site import main_site_index
from create_project import add_project
from build_query import build_query
from get_oauth_twitter import get_oauth_twitter

app.register_blueprint(auth_flask_login)
app.register_blueprint(main_site_index)
app.register_blueprint(add_project)
app.register_blueprint(build_query)
app.register_blueprint(get_oauth_twitter)

manager = Manager(app)

manager.add_command('runserver', Server(
                    use_debugger= True,
                    use_reloader = True,
                    host = '0.0.0.0'
                    )
)


if __name__ == '__main__':
    manager.run()