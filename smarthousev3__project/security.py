from flask import Blueprint, Response, request, session, jsonify
from database import connect_db
from PIL import Image
import numpy as np
import cv2
import torch
from facenet_pytorch import MTCNN
from sklearn.metrics.pairwise import cosine_similarity
import io
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
from botmes import send_telegram_message
security_bp = Blueprint("security", __name__)

# === Cấu hình ===
THRESHOLD = 0.7
camera_on = False
cap = None
motion_detection_enabled = True
security_alert_count = 0

# === Thiết bị và mô hình ===
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
face_model = torch.load("models/face_model_feature_v3.pth", map_location=device)
face_model.eval()
mtcnn = MTCNN(keep_all=False, device=device)

# === Trích embedding khuôn mặt ===
def get_face_embedding(image_pil):
    try:
        face = mtcnn(image_pil)
        if face is None:
            return None
        face = face.unsqueeze(0).to(device)
        with torch.no_grad():
            embedding = face_model(face).cpu().numpy().flatten()
        return embedding
    except Exception as e:
        print(f"Lỗi xử lý ảnh: {e}")
        return None

# === Gửi email cảnh báo ===

# === Tải khuôn mặt đã lưu ===


# def load_all_user_faces():
#     conn = connect_db()
#     cursor = conn.cursor()
#     cursor.execute("SELECT face_encoding FROM user_faces")
#     records = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     embeddings = [np.array(json.loads(r[0])) for r in records if r[0]]
#     return embeddings

import json
import numpy as np
import sqlite3  # Hoặc thư viện bạn sử dụng để kết nối cơ sở dữ liệu, ví dụ MySQL hoặc PostgreSQL


def load_all_user_faces():
    # Kết nối đến cơ sở dữ liệu
    conn = connect_db()
    cursor = conn.cursor()

    # Thực thi truy vấn để lấy tất cả các encoding khuôn mặt
    cursor.execute("SELECT face_encoding FROM user_faces")
    records = cursor.fetchall()

    # Đóng kết nối cơ sở dữ liệu
    cursor.close()
    conn.close()

    # Chuyển các chuỗi JSON thành numpy array
    embeddings = []
    for r in records:
        if r[0]:  # Kiểm tra xem dữ liệu có tồn tại
            try:
                # Giải mã chuỗi JSON và chuyển thành numpy array
                embedding = np.array(json.loads(r[0]))
                embeddings.append(embedding)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON for record: {r[0]} - {e}")
    
    return embeddings


# === Nhận diện người dùng ===
def recognize_face(face_embedding, known_embeddings):
    if known_embeddings.size == 0:
        return "Unknown"
    similarities = cosine_similarity([face_embedding], known_embeddings)[0]
    max_sim = np.max(similarities)
    if max_sim < THRESHOLD:
        return "Unknown"
    return "Member"



def gen_frames():
    global cap, camera_on
    known_embeddings = np.array(load_all_user_faces())
    last_detected_unknown = False

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes, _ = mtcnn.detect(frame_rgb)

        if boxes is not None:
            for box in boxes:
                x1, y1, x2, y2 = map(int, box)
                face = frame_rgb[y1:y2, x1:x2]
                if face.shape[0] < 10 or face.shape[1] < 10:
                    continue
                face_resized = cv2.resize(face, (160, 160))
                face_tensor = torch.tensor(face_resized).permute(2, 0, 1).unsqueeze(0).float().to(device) / 255.0
                with torch.no_grad():
                    embedding = face_model(face_tensor).cpu().numpy().flatten()
                name = recognize_face(embedding, known_embeddings)
                if motion_detection_enabled:
                    if name == "Unknown":  
                        if not last_detected_unknown:
                            send_telegram_message()
                            last_detected_unknown = True  
                    else:
                        last_detected_unknown = False 
                color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        cv2.imshow('Face Recognition', frame)


        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# === API ===
@security_bp.route('/start_camera', methods=['POST'])
def start_camera():
    global cap, camera_on
    
    # Kiểm tra xem camera đã bật hay chưa
    if not camera_on:
        cap = cv2.VideoCapture(0)  # Mở camera mặc định (ID 0)
        
        # Kiểm tra xem camera có mở thành công không
        if not cap.isOpened():
            return jsonify({"status": "error", "message": "Không thể mở camera"}), 500
        
        camera_on = True
        return jsonify({"status": "camera_started"})
    
    # Nếu camera đã bật rồi
    return jsonify({"status": "camera_already_started"})

@security_bp.route('/stop_camera', methods=['POST'])
def stop_camera():
    global cap, camera_on
    if cap and camera_on:
        cap.release()
        camera_on = False
    return jsonify({"status": "camera_stopped"})

@security_bp.route('/update-motion-detection', methods=['POST'])
def update_motion_detection():
    global motion_detection_enabled
    data = request.get_json()
    motion_detection_enabled = data.get("enabled", True)
    return jsonify({"motion_detection": motion_detection_enabled})

@security_bp.route('/video_feed')
def video_feed():
    global camera_on
    if not camera_on:
        return "Camera chưa được bật", 400
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@security_bp.route('/get-alert-count')
def get_alert_count():
    return jsonify({"count": security_alert_count})
