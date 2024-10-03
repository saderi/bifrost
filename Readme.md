# Bifrost

Some countries have restrictions on the internet, and some services are blocked. This can be a problem when you need to send a message to a chat, or make a request to a service. this is where bifrost comes in.

This is a simple API to pypass API calls to some services, for now it only has a endpoint to send messages to a telegram chat. but it can be easily extended to other services.

**Note:** Its not stored any chat or other information, it just forwards the message to the service. but in the future i'll try to find a way to prevent any kind of MITM attack.


## Setup

1. **Clone the repository and Create and activate a virtual environment
    ```sh
    git clone https://github.com/saderi/bifrost.git /opt/bifrost
    cd /opt/bifrost
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Create a `.env` file:**
    ```sh
    cp .env.example .env
    ```
    Update `TOKEN_SECRET` in the `.env` file. this token will be used to authenticate the requests. IS NOT RELATED TO THE TELEGRAM TOKEN.
## Running the Application

1. **Start the Flask application:**
    ```sh
    flask run --host=0.0.0.0 --port=5000
    ```

2. **Start the service using systemd:**
    ```sh
    sudo cp bifrost.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl start bifrost.service
    sudo systemctl enable bifrost.service
    ```

## Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/` | POST/GET | Health check endpoint. |
| `/send_telegram` | POST | Restart API and Worker services. |


## send_telegram
You can send a message to a telegram chat using this endpoint. requieres fields:
- `chat_id`: The chat id of the chat you want to send the message to.
- `message`: The message you want to send.
- `telegram_bot_token`: The token of the bot you want to use to send the message.


Example request:
```bash
curl --location 'http://127.0.0.1:5000/send_telegram' \
--request POST \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer YOUR_SECRET_TOKEN_HERE' \
--data '{
    "telegram_bot_token": "9999999999:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "telegram_chat_id": "-11111111111",
    "text": "YOUR TEST"
}'
```

Response will be exactly the response from the telegram API.
