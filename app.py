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
            return User(info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[8], info[9], info[10], info[11], info[12], info[13], info[14], info[15])
        else:
            print("Failed for some reason (or just not logged in)")
            return None
    
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from dashboard import dash as dash_blueprint
    app.register_blueprint(dash_blueprint)

    from profile_symptoms import ps as ps_blueprint
    app.register_blueprint(ps_blueprint)

    from video import vid as vid_blueprint
    app.register_blueprint(vid_blueprint)

    return app