FROM python:3.8-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

ENV API_ACCESS_TOKEN=shhh_its_a_secret_token

# Run flask app
CMD ["flask", "run", "--host=0.0.0.0"]