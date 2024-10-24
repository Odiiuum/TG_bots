import requests
import os
from flask import Flask, request

from config_reader import config

app = Flask(__name__)

def send_telegram_message(message, chat_id):
    url = f'https://api.telegram.org/bot{config.bot_token.get_secret_value()}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=data)

def decode_ucs2(hex_str):
    try:
        decoded_str = bytes.fromhex(hex_str).decode('utf-16-be')
    except (ValueError, UnicodeDecodeError):
        decoded_str = hex_str
    return decoded_str
    
@app.route('/sms', methods=['POST'])
def sms_handler():
    response = request.get_data()
    hex_str = response.decode('utf-8') 
    lines = hex_str.split('\n') 
    message_content = decode_ucs2(lines[-1])
    lines[-1] = message_content
    result = '\n'.join(lines)
    send_telegram_message(result, "-1002460455678")
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
