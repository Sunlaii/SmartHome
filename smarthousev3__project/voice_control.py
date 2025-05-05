from flask import Blueprint, jsonify
import speech_recognition as sr
from servo_control import move_servo , controdevie
import sys
sys.stdout.reconfigure(encoding='utf-8')
voice_bp = Blueprint('voice', __name__)

recognizer = sr.Recognizer()

deviceStates = {
    "quạt": False  # mặc định là tắt
}


@voice_bp.route('/voice_recognition', methods=['GET'])
def voice_recognition():
    with sr.Microphone() as source:
        print("Đang lắng nghe...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Thử nhận diện tiếng Việt
        command_vn = recognizer.recognize_google(audio, language="vi-VN")
        # controdevie(command_vn)
        print(f"Tiếng Việt nhận được: {command_vn}")
        return jsonify({"text": command_vn, "lang": "vi"})
    except sr.UnknownValueError:
        try:
            # Nếu tiếng Việt không được, thử tiếng Anh
            command_en = recognizer.recognize_google(audio, language="en-US")
            # controdevie(command_en)
            print(f"English recognized: {command_en}")
            return jsonify({"text": command_en, "lang": "en"})
        except sr.UnknownValueError:
            print("Không nhận diện được giọng nói.")
            return jsonify({"text": None, "lang": None})

