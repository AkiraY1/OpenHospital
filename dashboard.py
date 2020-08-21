from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_required, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from models import User
import random
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

dashboard = Blueprint('dashboard', __name__)