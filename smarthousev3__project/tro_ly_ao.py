# from flask import Blueprint, jsonify,request,Flask 
# import speech_recognition as sr
# import pyttsx3
# import requests
# from datetime import datetime
# import threading
# import time
# import json
# import os
# import re
# voice_bp = Blueprint('voice_assistant', __name__)

# recognizer = sr.Recognizer()
# engine = pyttsx3.init()

# latest_voice_command = None
# scheduled_event = []
# scheduled_event_file = "scheduled_events.json"
# voice_log_file = "voice_log.txt"

# # === Cấu hình giọng nói ===
# def configure_voice():
#     try:
#         voices = engine.getProperty('voices')
#         for voice in voices:
#             if 'vi' in voice.name.lower() or 'vietnam' in voice.name.lower():
#                 engine.setProperty('voice', voice.id)
#                 break
#         engine.setProperty('rate', 140)
#         engine.setProperty('volume', 0.9)
#     except Exception as e:
#         print("Lỗi cấu hình giọng nói:", e)

# configure_voice()

# def speak_text(text):
#     try:
#         engine.say(text)
#         engine.runAndWait()
#     except Exception as e:
#         print("Lỗi phát âm:", e)

# def log_voice_command(command_text):
#     try:
#         with open(voice_log_file, "a", encoding="utf-8") as f:
#             timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             f.write(f"[{timestamp}] {command_text}\n")
#     except Exception as e:
#         print("Lỗi ghi log:", e)

# def get_weather(city):
#     api_key = "a3e670ab8298b8320c68c28054cae417"  # dùng thử - thay bằng API key của bạn
#     url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=vi"
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             temp = data['main']['temp']
#             humidity = data['main']['humidity']
#             description = data['weather'][0]['description']
#             wind = data['wind']['speed']
#             return (f"Thời tiết tại {city}:\n"
#                     f"- Trạng thái: {description}\n"
#                     f"- Nhiệt độ: {temp}°C\n"
#                     f"- Độ ẩm: {humidity}%\n"
#                     f"- Gió: {wind} m/s")
#         else:
#             return f"Không tìm thấy thông tin thời tiết cho {city}"
#     except Exception as e:
#         return f"Lỗi khi lấy thời tiết: {str(e)}"

# def load_scheduled_events():
#     if os.path.exists(scheduled_event_file):
#         try:
#             with open(scheduled_event_file, "r", encoding="utf-8") as f:
#                 data = json.load(f)
#                 for item in data:
#                     event_time = datetime.strptime(item["event_time"], "%Y-%m-%d %H:%M:%S")
#                     scheduled_event.append((event_time, item["event_description"]))
#         except Exception as e:
#             print("Lỗi khi tải lịch:", e)

# def save_scheduled_events():
#     try:
#         data = [{"event_time": et.strftime("%Y-%m-%d %H:%M:%S"), "event_description": desc}
#                 for et, desc in scheduled_event]
#         with open(scheduled_event_file, "w", encoding="utf-8") as f:
#             json.dump(data, f, ensure_ascii=False, indent=4)
#     except Exception as e:
#         print("Lỗi khi lưu lịch:", e)

# def schedule_event(event_time, event_description):
#     scheduled_event.append((event_time, event_description))
#     save_scheduled_events()
#     return f"Đã lên lịch sự kiện '{event_description}' vào {event_time.strftime('%d/%m %H:%M')}"

# def notify_events():
#     while True:
#         now = datetime.now()
#         for event in scheduled_event[:]:
#             event_time, description = event
#             if now >= event_time:
#                 speak_text(f"Chuông báo: sự kiện {description} đã đến giờ.")
#                 print(f"Sự kiện {description} đã đến giờ.")
#                 scheduled_event.remove(event)
#                 save_scheduled_events()
#         time.sleep(30)
# def process_voice_command(command):
#     command = command.lower()
#     normalized_command = remove_vietnamese_tones(command)

#     is_turn_on = "bat" in normalized_command
#     is_turn_off = "tat" in normalized_command

#     devices = {
#         "den": "light",
#         "quat": "fan",
#         "may lanh": "air_conditioner"
#     }

#     for device_key, device_endpoint in devices.items():
#         if device_key in normalized_command:
#             action = "on" if is_turn_on else "off" if is_turn_off else None
#             if action:
#                 try:
#                     url = f"http://localhost:5000/control_device/{device_endpoint}/{action}"
#                     requests.get(url)
#                     speak_text(f"Đã {action} {device_key}")
#                 except Exception as e:
#                     print("Lỗi gửi yêu cầu điều khiển:", e)
#                 return

#     speak_text("Tôi chưa hiểu thiết bị bạn muốn điều khiển.")
# def remove_vietnamese_tones(txt):
#     txt = txt.lower()
#     patterns = {
#         '[áàảãạăắằẳẵặâấầẩẫậ]': 'a',
#         '[éèẻẽẹêếềểễệ]': 'e',
#         '[íìỉĩị]': 'i',
#         '[óòỏõọôốồổỗộơớờởỡợ]': 'o',
#         '[úùủũụưứừửữự]': 'u',
#         '[ýỳỷỹỵ]': 'y',
#         '[đ]': 'd'
#     }
#     for regex, replace in patterns.items():
#         txt = re.sub(regex, replace, txt)
#     return txt        

# # === API ===

# @voice_bp.route('/voice_recognition')
# def voice_recognition_api():
#     global latest_voice_command
#     with sr.Microphone() as source:
#         recognizer.adjust_for_ambient_noise(source)
#         try:
#             speak_text("Tôi đang lắng nghe...")
#             audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
#             text = recognizer.recognize_google(audio, language="vi-VN")
#             print("Bạn đã nói:", text)
#             log_voice_command(text)
#             latest_voice_command = text

#             # 👉 Thêm dòng xử lý lệnh giọng nói
#             process_voice_command(text)

#             return jsonify({"text": text})
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500


# @voice_bp.route('/get_voice_command')
# def get_voice_command():
#     global latest_voice_command
#     if latest_voice_command:
#         result = {"text": latest_voice_command}
#         latest_voice_command = None
#         return jsonify(result)
#     return jsonify({})

# @voice_bp.route('/get_voice_log')
# def get_voice_log():
#     try:
#         if os.path.exists(voice_log_file):
#             with open(voice_log_file, "r", encoding="utf-8") as f:
#                 lines = f.readlines()[-50:]
#                 return jsonify({"log": lines[::-1]})
#         else:
#             return jsonify({"log": []})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # === Khởi động thread nhắc lịch (chạy nền)
# def init_voice_assistant():
#     load_scheduled_events()
#     threading.Thread(target=notify_events, daemon=True).start()
