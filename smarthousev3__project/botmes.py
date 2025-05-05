import requests
from datetime import datetime

BOT_TOKEN = '7583883761:AAHWnRFSYSgYHK82KvUy35fdLQ5S4dukn5w'
CHAT_ID = '7499111381'    
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
MESSAGE = f'Phat hien unknow tu camera anninh :{current_time}'

def send_telegram_message():
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': MESSAGE
    }
    response = requests.post(url, data=payload)
    return response.json()


