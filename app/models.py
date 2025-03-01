from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

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

# User loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))