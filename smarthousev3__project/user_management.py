from flask import Blueprint, request, jsonify, session
from database import connect_db
import base64

import io
from PIL import Image
import numpy as np

user_management_bp = Blueprint('user_management', __name__)

# ===========================
# Lấy danh sách người dùng (trừ admin)
# ===========================
@user_management_bp.route('/api/users')
def get_users():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email, pass, status, phone, address, CCCD FROM users WHERE role != 'admin'")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)


# ===========================
# Thêm người dùng mới
# ===========================
@user_management_bp.route('/api/users/add', methods=['POST'])
def add_user():
    data = request.form  # dùng request.form để tương thích FormData
    name = data.get('name')
    address = data.get('address')
    email = data.get('email')
    password = data.get('pass')
    phone = data.get('phone')
    cccd = data.get('cccd')

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (name, address, email, pass, phone, role, status, CCCD)
            VALUES (%s, %s, %s, %s, %s, 'user', 'Hoạt động', %s)
        """, (name, address, email, password, phone, cccd))
        conn.commit()
        return jsonify({"success": True, "message": "Người dùng đã được thêm thành công."}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# ===========================
# Cập nhật người dùng (admin hoặc người dùng tự sửa)
# ===========================
@user_management_bp.route('/api/users/update', methods=['POST'])
def update_user():
    # Phân biệt xem là JSON hay form
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    user_id = data.get("id")  # nếu không có ID nghĩa là cập nhật chính mình

    # Nếu không có id => dùng email từ session
    if not user_id:
        email = session.get("email")
        if not email:
            return jsonify({"success": False, "message": "Chưa đăng nhập!"}), 401
        condition_field, condition_value = "email", email
    else:
        condition_field, condition_value = "id", user_id

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(f"""
            UPDATE users SET name=%s, pass=%s, phone=%s, address=%s
            WHERE {condition_field}=%s
        """, (data["name"], data["pass"], data["phone"], data["address"], condition_value))
        conn.commit()
        cursor.close()
        conn.close()

        if not user_id:
            session["name"] = data["name"]  # cập nhật tên trong session nếu chính mình

        return jsonify({"success": True, "message": "Cập nhật thành công!"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500



# ===========================
# Xóa người dùng
# ===========================
@user_management_bp.route('/api/users/delete', methods=['POST'])
def delete_user():
    data = request.get_json()
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (data['id'],))
        conn.commit()
        return jsonify({"success": True, "message": "Xóa thành công!"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ===========================
# Lấy thông tin người dùng hiện tại
# ===========================
@user_management_bp.route('/api/users/profile', methods=['GET'])
def get_user_profile():
    email = session.get("email")
    if not email:
        return jsonify({"success": False, "message": "Chưa đăng nhập!"}), 401

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name, email, pass, phone, address FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(user), 200

