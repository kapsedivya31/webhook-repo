# Webhook Receiver

This Flask app receives GitHub Webhooks for Push and Pull Request events from `action-repo` and saves them to MongoDB Atlas. A simple UI displays the latest events.

## How to run locally

1. Clone the repo.
2. Install dependencies:

### pip install -r requirements.txt

3. Add your MongoDB URI in `app.py`.
4. Run Flask:

### python app.py

5. Start ngrok:

### ngrok http 5000

6. Add the ngrok HTTPS URL + `/webhook` as a webhook in `action-repo`.

## Author

Divya Kapse
