import os
from flask import Flask, request, jsonify, send_from_directory
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)

# -------------------------
# Routes
# -------------------------

@app.route('/')
def index():
    return send_from_directory('.', 'sendmail.html')

@app.route('/success.html')
def success_page():
    return send_from_directory('.', 'success.html')

@app.route('/send', methods=['POST'])
def send_email():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()

    if not name or not email:
        return jsonify({"error": "Name and email required"}), 400

    try:
        send_confirmation_email(name, email)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------
# Email function
# -------------------------
def send_confirmation_email(name, email):
    msg = Message(subject='[Shopee] Your account has been compromised',
                  recipients=[email])
    msg.html = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.6;">
        <div style="max-width:600px;margin:0 auto;padding:20px;border:1px solid #ddd;">
            <div style="background-color:#ee4d2d;padding:15px;text-align:center;">
                <h1 style="color:#fff;margin:0;">Shopee</h1>
            </div>
            <div style="padding:20px;">
                <p>Hi {name},</p>
                <p>Dear Shopee customer,</p> 
                <p>your account has been compromised. Please take immediate action to secure your account.</p>
                <p>Your password has been changed. You have 24 hours to solve the problem or your account will be locked</p>\
                <p>Reset your password now to secure your account.</p>
                <div style="text-align:center;margin-top:30px;">
                    <a href="#" style="background-color:#ee4d2d;color:#fff;padding:10px 20px;text-decoration:none;border-radius:5px;">Reset password</a>
                </div>
            </div>
            <div style="background-color:#f4f4f4;padding:15px;text-align:center;font-size:12px;color:#666;">
                <p>Follow us on:</p>
                <p>
                    <a href="#" style="text-decoration:none;color:#333;">Facebook</a> |
                    <a href="#" style="text-decoration:none;color:#333;">Instagram</a> |
                    <a href="#" style="text-decoration:none;color:#333;">Twitter</a>
                </p>
                <p>&copy; 2025 Shopee. All rights reserved.</p>
            </div>
        </div>
    </div>
    """
    mail.send(msg)

# -------------------------
# Run server
# -------------------------
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050, debug=True)
