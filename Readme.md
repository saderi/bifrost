# Bifrost

Some countries have restrictions on the internet, and some services are blocked. This can be a problem when you need to send a message to a chat, or make a request to a service. this is where bifrost comes in.

This is a simple API to pypass API calls to some services, for now it only has a endpoint to send messages to a telegram chat. but it can be easily extended to other services.

**Note:** It doesn't store any information; it just forwards the message to the service. However, in the future, I may try to find a way to prevent any kind of MITM attack.

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
    Update `TOKEN_SECRET` in the `.env` file. this token will be used to authenticate the requests.
    
    **NOTE:** This token is not related to requests you want to send, its just for this API to authenticate the requests.
## Running the Application

Start the Flask application for development

```sh
flask run
```

**Some notes for production:**

If you want to run it in production do not expose the flask app directly to the internet, use a reverse proxy like nginx or apache.

You can get systemd service file from the repository and use it to start the service using systemd.

```sh
sudo cp bifrost.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start bifrost.service
sudo systemctl enable bifrost.service
```

## Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/` | GET | Health check endpoint. |
| `/send` | GET, POST | Send GET and POST to a URL. |
| `/send_telegram` | POST | Send a message to a telegram chat. |

## Send request to a URL
You can send a GET or POST request to a URL using `/send`  endpoint. json example:
```json
{
    "url": "TARGET_API_URL",
    "headers": {
        "Content-Type": "application/json",
        "Authorization": "Bearer TARGET_API_TOKEN if needed"
    },
    "json_payload": {
            "field1": "value1",
            "field2": "value2"
        }
}
```

**Important Notes:**
* Only `url` is required, `headers` and `json_payload` are optional. 
* method will be determined by the method of the request.
* `json_payload` will be sent only if the request is a POST request as a json payload.
* response will be exactly the response from the target API with the status code.


## Send a message to a telegram chat
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
