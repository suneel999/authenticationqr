from flask import Blueprint, render_template, request, send_file, redirect, url_for, flash
import qrcode
import io
import base64
from datetime import datetime
from app import db
from app.models import User, QRLog
from app.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

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
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')
            img_io = io.BytesIO()
            img.save(img_io, 'PNG')
            img_io.seek(0)

            # Encode to Base64
            qr_img_b64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

            # Log the QR code generation
            qr_log = QRLog(data=qr_data, qr_image=qr_img_b64, user_id=current_user.id)
            db.session.add(qr_log)
            db.session.commit()

    return render_template('index.html', qr_img_b64=qr_img_b64, qr_data=qr_data)

@main_routes.route('/download_qr', methods=['POST'])
def download_qr():
    qr_data = request.form.get('qr_data')
    if qr_data:
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        # Send the QR code as a downloadable file
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
    # Fetch all QR logs for the current user
    user_logs = QRLog.query.filter_by(user_id=current_user.id).order_by(QRLog.timestamp.desc()).all()
    return render_template('logs.html', logs=user_logs)

# Auth routes
@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@auth_routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))
