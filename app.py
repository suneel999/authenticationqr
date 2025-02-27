from flask import Flask, render_template, request, send_file
import qrcode
import io
import base64


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    qr_img_b64 = None
    qr_data = ""

    if request.method == 'POST':
        qr_data = request.form.get('qr_data')
        print("Received QR Data:", qr_data)  # Debugging print

        if qr_data:
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
            print("Generated QR Base64:", qr_img_b64[:50])  # Print first 50 chars for debugging

    return render_template('index.html', qr_img_b64=qr_img_b64, qr_data=qr_data)

@app.route('/download_qr', methods=['POST'])
def download_qr():
    qr_data = request.form.get('qr_data')
    if qr_data:
        qr = qrcode.make(qr_data)
        img_io = io.BytesIO()
        qr.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='qrcode.png')
    return "Invalid request", 400

if __name__ == '__main__':
    app.run(debug=True)