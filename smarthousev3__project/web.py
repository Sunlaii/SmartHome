from flask import Flask
from login import login_bp  # ✅ Import Blueprint từ login.py
from devices import devices_bp  # ✅ Import Blueprint từ devices.py
from face_auth import face_auth_bp  # Import Blueprint
from user_management import user_management_bp  # ✅ Thêm dòng này
from voice_control import voice_bp
from security import security_bp
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
app.secret_key = 'supersecretkey'  # Để sử dụng session

# 👉 Đăng ký Blueprint login
app.register_blueprint(login_bp)
# 👉 Đăng ký Blueprint cho devices
app.register_blueprint(devices_bp)
# Đăng ký Blueprint

app.register_blueprint(face_auth_bp)
app.register_blueprint(user_management_bp)  # ✅ Đăng ký blueprint mới
app.register_blueprint(voice_bp)
app.register_blueprint(security_bp, url_prefix="/security")
if __name__ == "__main__":
    app.run(debug=True,use_reloader=False)

