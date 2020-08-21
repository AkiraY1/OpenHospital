from flask import Blueprint, render_template, url_for
from flask_login import login_required, current_user

ps = Blueprint('ps', __name__)

@ps.route('/profile')
@login_required
def profile():
    return render_template('profile.html')