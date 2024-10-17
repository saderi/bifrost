import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
API_ACCESS_TOKEN = os.getenv('API_ACCESS_TOKEN', 'default_secret_token')


def authenticate(f):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Unauthorized"}), 401
        token = auth_header.split(' ')[1]
        if token != API_ACCESS_TOKEN:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route('/send_telegram', methods=['POST'])
@authenticate
def send_telegram():
    data = request.get_json()
    telegram_bot_token = data.get('telegram_bot_token')
    telegram_chat_id = data.get('telegram_chat_id')
    text = data.get('text')

    if not text:
        return jsonify({"error": "Text is required"}), 400
    if not telegram_bot_token:
        return jsonify({"error": "Telegram bot token is required"}), 400
    if not telegram_chat_id:
        return jsonify({"error": "Telegram chat ID is required"}), 400

    url = f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage'
    payload = {
        'chat_id': telegram_chat_id,
        'text': text
    }
    response = requests.post(url, json=payload)
    return response.json()

@app.route('/send', methods=['POST', 'GET'])
@authenticate
def send_post():
    method = request.method
    data = request.get_json()
    url = data.get('url')
    json_payload = data.get('json_payload')
    headers = data.get('headers') if data.get('headers') else None
    if url is None:
        return jsonify({"error": "URL is required"}), 400
    
    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'POST':
        response = requests.post(url, json=json_payload, headers=headers)
    else:
        return jsonify({"error": f"Method {method} is not supported"}), 400
    
    return response.json(), response.status_code


@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Hello, World!"}), 200

if __name__ == '__main__':
    app.run()