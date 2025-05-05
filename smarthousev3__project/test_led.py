from pyfirmata2 import Arduino
import time

# Khởi tạo kết nối với Arduino
board = Arduino('COM15')  # Thay COM15 bằng cổng Arduino của bạn
led_pin = 3  # Chân số 3

# Cấu hình chân LED là OUTPUT
board.digital[led_pin].mode = 1

def blink_led():
    """Hàm làm LED nhấp nháy."""
    try:
        while True:
            board.digital[led_pin].write(1)  # Bật LED
            time.sleep(1)  # Chờ 1 giây
            board.digital[led_pin].write(0)  # Tắt LED
            time.sleep(1)  # Chờ 1 giây
    except KeyboardInterrupt:
        print("Dừng nhấp nháy LED.")
        board.exit()

if __name__ == "__main__":
    blink_led()