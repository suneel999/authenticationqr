import qrcode
import io
import base64
from datetime import datetime
from app import db
from app.models import QRLog

def generate_qr_code(qr_data, user_id):
  
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
    qr_log = QRLog(data=qr_data, qr_image=qr_img_b64, user_id=user_id)
    db.session.add(qr_log)
    db.session.commit()

    return qr_img_b64

def download_qr_code(qr_data):
    
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

    return img_io

def get_user_qr_logs(user_id):
    
    return QRLog.query.filter_by(user_id=user_id).order_by(QRLog.timestamp.desc()).all()
