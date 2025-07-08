from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Replace this with your MongoDB Atlas URI
client = MongoClient("YOUR_MONGODB_URI")
db = client['webhooks_db']
collection = db['events']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(data)

    # Extract useful info (simplified example)
    event_type = request.headers.get('X-GitHub-Event')

    author = data['pusher']['name'] if 'pusher' in data else 'Unknown'
    timestamp = datetime.utcnow().isoformat()

    doc = {
        'author': author,
        'action': event_type,
        'from_branch': '',
        'to_branch': '',
        'timestamp': timestamp
    }

    # Add branches if needed (you can improve this later)
    collection.insert_one(doc)

    return '', 200

@app.route('/data')
def get_data():
    events = list(collection.find().sort('timestamp', -1).limit(10))
    for e in events:
        e['_id'] = str(e['_id'])
    return jsonify(events)

if __name__ == '__main__':
    app.run(port=5000)
