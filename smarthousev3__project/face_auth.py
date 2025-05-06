from flask import Blueprint, request, jsonify
import base64
import io
import numpy as np
from PIL import Image
import torch
from facenet_pytorch import MTCNN
from sklearn.metrics.pairwise import cosine_similarity
import json
from database import connect_db

face_auth_bp = Blueprint("face_auth", __name__)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
face_model = torch.load("models/face_model_feature_v3.pth", map_location=device)
face_model.eval()

mtcnn = MTCNN(keep_all=False, device=device)
THRESHOLD = 0.7

def get_face_embedding(image_bytes):
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        face = mtcnn(img)
        if face is None:
            return None
        face = face.unsqueeze(0).to(device)
        with torch.no_grad():
            embedding = face_model(face).cpu().numpy().flatten()
        return embedding
    except Exception as e:
        print(f"Lỗi xử lý ảnh: {e}")
        return None

# === Đăng ký khuôn mặt ===
@face_auth_bp.route('/api/users/upload-face', methods=['POST'])
def upload_face_image():
    data = request.get_json()
    email = data.get("email")
    image_data = data.get("image")

    if not email or not image_data:
        return jsonify({"success": False, "message": "Thiếu email hoặc ảnh!"}), 400

    try:
        if ',' in image_data:
            image_data = image_data.split(",")[1]
        decoded = base64.b64decode(image_data)

        embedding = get_face_embedding(decoded)
        if embedding is None:
            return jsonify({"success": False, "message": "Không phát hiện khuôn mặt!"}), 400

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO user_faces (email, image, face_encoding)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                image = VALUES(image),
                face_encoding = VALUES(face_encoding)
        """, (email, decoded, json.dumps(embedding.tolist())))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"success": True, "message": "Lưu encoding khuôn mặt thành công!"}), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Lỗi xử lý ảnh: {str(e)}"}), 500

# === Đăng nhập bằng khuôn mặt ===
@face_auth_bp.route('/api/users/login-face', methods=['POST'])
def login_with_face():
    data = request.get_json()
    image_data = data.get("image")

    if not image_data:
        return jsonify({"success": False, "message": "Thiếu ảnh!"}), 400

    try:
        if ',' in image_data:
            image_data = image_data.split(",")[1]
        decoded = base64.b64decode(image_data)

        input_embedding = get_face_embedding(decoded)
        if input_embedding is None:
            return jsonify({"success": False, "message": "Không phát hiện khuôn mặt!"}), 400

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT email, face_encoding FROM user_faces WHERE face_encoding IS NOT NULL")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        for email, stored_encoding in rows:
            known_embedding = np.array(json.loads(stored_encoding))
            similarity = cosine_similarity([input_embedding], [known_embedding])[0][0]
            if similarity >= THRESHOLD:
                return jsonify({"success": True, "message": "Đăng nhập thành công!", "email": email}), 200

        return jsonify({"success": False, "message": "Không tìm thấy người dùng phù hợp!"}), 401

    except Exception as e:
        return jsonify({"success": False, "message": f"Lỗi xử lý ảnh: {str(e)}"}), 500
