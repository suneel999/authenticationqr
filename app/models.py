from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
import pytz  # Import pytz for timezone handling

class User(db.Model, UserMixin):  # Inherit from UserMixin
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    qr_logs = db.relationship('QRLog', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class QRLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(500), nullable=False)
    qr_image = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"QRLog('{self.data}', '{self.timestamp}')"

    # Add the get_ist_timestamp method
    def get_ist_timestamp(self):
        utc_time = self.timestamp
        ist_timezone = pytz.timezone('Asia/Kolkata')  # Define IST timezone
        ist_time = utc_time.replace(tzinfo=pytz.utc).astimezone(ist_timezone)  # Convert to IST
        return ist_time.strftime('%Y-%m-%d %H:%M:%S')  # Format the timestamp

# User loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
