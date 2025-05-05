
from pyfirmata2 import Arduino
import time

from flask import Flask, request, jsonify


board = Arduino('COM15')  # Thay COM11 bằng cổng Arduino của bạn
servo_pin = 9  # Chân 9 ở chế độ servo

def move_servo(angle):
    """Di chuyển servo đến góc chỉ định."""
    board.servo_config(servo_pin)
    board.digital[servo_pin].write(angle)  # Chuyển đổi góc trực tiếp cho servo
    time.sleep(1)


def controdevie(action):
    if "open" in action.lower():
        move_servo(90)
       
    elif "finish" in action.lower():
        move_servo(0)




def main():
    while True:
        # Nhập lệnh từ người dùng
        action = input("Nhập lệnh (bật/tắt): ").strip().lower()
        
        # Kiểm tra điều kiện dừng chương trình
        if action == 'exit':
            print("Đang thoát chương trình...")
            break
        
        # Gọi hàm điều khiển thiết bị
        controdevie(action)
if __name__ == "__main__":
    main()