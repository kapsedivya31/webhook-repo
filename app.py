from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# ✅ Replace with your real password
client = MongoClient("mongodb+srv://kapsedivya55:8mvxzL24Wpj0UsHl@eventcluster.o7ino.mongodb.net/?retryWrites=true&w=majority&appName=eventcluster")
db = client['webhooks_db']
collection = db['events']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        print("Received:", data)

        event_type = request.headers.get('X-GitHub-Event', 'unknown')

        author = 'Unknown'
        if 'pusher' in data:
            author = data['pusher']['name']
        elif 'pull_request' in data and 'user' in data['pull_request']:
            author = data['pull_request']['user']['login']

        from_branch = ''
        to_branch = ''

        if event_type == 'push':
            to_branch = data['ref'].split('/')[-1]
        elif event_type == 'pull_request':
            from_branch = data['pull_request']['head']['ref']
            to_branch = data['pull_request']['base']['ref']

        doc = {
            'author': author,
            'action': event_type,
            'from_branch': from_branch,
            'to_branch': to_branch,
            'timestamp': datetime.utcnow().isoformat()
        }

        collection.insert_one(doc)
        print("Saved:", doc)

        return '', 200

    except Exception as e:
        print("Webhook error:", e)
        return 'Error', 500

@app.route('/data')
def get_data():
    try:
        events = list(collection.find().sort('timestamp', -1).limit(10))
        for e in events:
            e['_id'] = str(e['_id'])
        return jsonify(events)
    except Exception as e:
        print("Data error:", e)
        return 'Error', 500

if __name__ == '__main__':
    app.run(port=5000)
