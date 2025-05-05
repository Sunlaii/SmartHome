from flask import Flask
from flask import Blueprint, jsonify
from pyfirmata2 import Arduino
import serial.tools.list_ports
from flask_cors import CORS
from flask import request
from servo_control import controdevie , move_servo


devices_bp = Blueprint("devices", __name__)


# # Tự động dò cổng Arduino
# def find_arduino_port():
#     ports = serial.tools.list_ports.comports()
#     for port in ports:
#         if "Arduino" in port.description or "CH340" in port.description:
#             return port.device
#     return None

# # Khởi tạo board nếu tìm thấy
# arduino_port = find_arduino_port()
# board = None
# light_pin = 13

# if arduino_port:
#     try:
#         board = Arduino(arduino_port)
#         board.digital[light_pin].mode = 1  # OUTPUT
#         print(f"Arduino kết nối tại {arduino_port}")
#     except Exception as e:
#         print("Lỗi khi kết nối Arduino:", e)
# else:
#     print("Không tìm thấy thiết bị Arduino nào.")

# @devices_bp.route('/control_light/<state>')
# def control_light(state):
#     if board:
#         if state == 'on':
#             board.digital[light_pin].write(1)
#         elif state == 'off':
#             board.digital[light_pin].write(0)
#         return jsonify({"status": state})
#     else:
#         return jsonify({"error": "Arduino không khả dụng"}), 503





@devices_bp.route('/control_device', methods=['POST'])
def control_device_api():
  
    data = request.get_json()
    action = data.get("action")

    if not action:
        return jsonify({"error": "Thiếu trường 'action'"}), 400

    try:
        controdevie(action)
        return jsonify({"status": "OK", "received": action})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


