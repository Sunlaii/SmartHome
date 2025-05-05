import os
import cv2
import numpy as np
import torch
from flask import Flask, request, jsonify
from PIL import Image
from facenet_pytorch import MTCNN
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Cấu hình thiết bị và mô hình
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
face_model = torch.load("face_model_feature_v3.pth", map_location=device)
face_model.eval()

mtcnn = MTCNN(keep_all=False, device=device)
THRESHOLD = 0.7

# === Hàm trích xuất đặc trưng khuôn mặt ===
def get_face_embedding(image_path):
    try:
        img = Image.open(image_path).convert("RGB")
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

# === Load dataset khuôn mặt ===
known_encodings = []
known_names = []
face_dir = "faces"

for filename in os.listdir(face_dir):
    if filename.lower().endswith((".jpg", ".png")):
        img_path = os.path.join(face_dir, filename)
        embedding = get_face_embedding(img_path)
        if embedding is not None:
            known_encodings.append(embedding)
            known_names.append(os.path.splitext(filename)[0])

# === API đăng nhập bằng khuôn mặt ===
@app.route('/face-login', methods=['POST'])
def face_login():
    file = request.files.get('image')
    if file is None:
        return jsonify({"error": "Thiếu ảnh"}), 400

    try:
        img = Image.open(file.stream).convert("RGB")
        face = mtcnn(img)
        if face is None:
            return jsonify({"error": "Không phát hiện khuôn mặt"}), 400

        face = face.unsqueeze(0).to(device)
        with torch.no_grad():
            input_embedding = face_model(face).cpu().numpy().flatten()

        name = "Unknown"
        for known_encoding, known_name in zip(known_encodings, known_names):
            sim = cosine_similarity([input_embedding], [known_encoding])[0][0]
            if sim >= THRESHOLD:
                name = known_name
                break

        if name == "Unknown":
            return jsonify({"error": "Xác thực thất bại"}), 401

        return jsonify({"message": "Đăng nhập thành công", "user": name})

    except Exception as e:
        return jsonify({"error": f"Lỗi xử lý ảnh: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
