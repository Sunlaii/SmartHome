from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from database import connect_db  # ✅ Import kết nối database

login_bp = Blueprint("login", __name__)  # ✅ Dùng Blueprint để tích hợp vào app.py

# 👉 Route hiển thị trang đăng nhập
@login_bp.route('/')
def login_page():
    return render_template('login.html')

# 👉 Route kiểm tra đăng nhập
@login_bp.route('/check-login', methods=['POST'])
def check_login():
    email = request.form.get("email")
    password = request.form.get("pass")

    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s AND pass = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            if user["status"] == "Bị khóa":
                return jsonify({"success": False, "message": "Tài khoản của bạn đã bị khóa!"})

            # Lưu session
            session["email"] = user["email"]
            session["name"] = user["name"]
            session["role"] = user["role"]

            return jsonify({"success": True, "role": user["role"], "name": user["name"]})

        return jsonify({"success": False, "message": "Sai email hoặc mật khẩu!"})

    except Exception as e:
        return jsonify({"success": False, "message": f"Lỗi hệ thống: {str(e)}"})

# 👉 Route trang admin
@login_bp.route('/admin')
def admin_page():
    if session.get("role") == "admin":
        return render_template('admin.html', name=session["name"])
    return redirect(url_for('login.login_page'))

# 👉 Route trang chính (user)
@login_bp.route('/index-vi')
def index_page():
    if session.get("email"):
        return render_template('index-vi.html', name=session["name"])
    return redirect(url_for('login.login_page'))
# 👉 Route đăng xuất
@login_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"success": True, "message": "Đăng xuất thành công!"})


