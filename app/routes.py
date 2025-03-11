from flask import Blueprint, render_template, request, send_file, redirect, url_for, flash
from flask_login import current_user, login_required
from app import db
from app.models import User, QRLog
from app.forms import RegistrationForm, LoginForm
from app.utils.qr_utils import generate_qr_code, download_qr_code, get_user_qr_logs
from app.utils.auth_utils import register_user, login_user_logic, logout_user_logic

# Create Blueprints
main_routes = Blueprint('main', __name__)
auth_routes = Blueprint('auth', __name__)

@main_routes.route('/', methods=['GET', 'POST'])
@login_required
def index():
    qr_img_b64 = None
    qr_data = ""

    if request.method == 'POST':
        qr_data = request.form.get('qr_data')
        if qr_data:
            qr_img_b64 = generate_qr_code(qr_data, current_user.id)

    return render_template('index.html', qr_img_b64=qr_img_b64, qr_data=qr_data)

@main_routes.route('/download_qr', methods=['POST'])
def download_qr():
    qr_data = request.form.get('qr_data')
    if qr_data:
        img_io = download_qr_code(qr_data)
        return send_file(
            img_io,
            mimetype='image/png',
            as_attachment=True,
            download_name='qrcode.png'
        )
    return "Invalid request", 400

@main_routes.route('/logs')
@login_required
def logs():
    user_logs = get_user_qr_logs(current_user.id)
    return render_template('logs.html', logs=user_logs)

# Auth routes
@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        return register_user(form)
    return render_template('register.html', title='Register', form=form)

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        return login_user_logic(form)
    return render_template('login.html', title='Login', form=form)

@auth_routes.route('/logout')
@login_required
def logout():
    return logout_user_logic()
