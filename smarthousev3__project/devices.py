from flask import Flask
from flask import Blueprint, jsonify
from pyfirmata2 import Arduino
import serial.tools.list_ports
from flask_cors import CORS
from flask import request
from servo_control import controdevie , move_servo


devices_bp = Blueprint("devices", __name__)






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




