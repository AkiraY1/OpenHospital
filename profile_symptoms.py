from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import login_required, current_user

ps = Blueprint('ps', __name__)

@ps.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    if current_user.role == 'Doctor' or 'Nurse':
        redirect(url_for('dashboard.dashboard'))
    print(request.form)
    return render_template('profile.html')