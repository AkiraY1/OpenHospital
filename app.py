from flask import Flask, Blueprint
from flask_login import LoginManager
import sqlite3

def create_app():
    app  = Flask(__name__)

    app.config['SECRET_KEY'] = 'mysecretkey'

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(id):
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        c = cur.execute('SELECT id from users WHERE id = (?)', [id])
        table_id = str(c.fetchone())
        good_id = table_id.strip('(),')
        if id == good_id:
            u = cur.execute('SELECT * from users WHERE id = (?)', [id])
            info = u.fetchone()
            return User(info[0], info[1], info[2], info[3], info[4], info[5]) # gotta fix this soon
        else:
            print("Failed for some reason")
            return None
    
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from dashboard import dashboard as dash_blueprint
    app.register_blueprint(dash_blueprint)

    from profile_symptoms import ps as ps_blueprint
    app.register_blueprint(ps_blueprint)

    return app