from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)


CORS(app, resources={r"/*": {"origins": "https://ui-components-ruddy.vercel.app"}})


client = MongoClient(os.environ.get("MONGO_URI"))
db = client.github_webhook
collection = db.actions

@app.route("/webhook", methods=["POST"])
def github_webhook():
    data = request.json

    try:
        action_type = data["action"]
        author = data["author"]
        from_branch = data.get("from_branch", "")
        to_branch = data["to_branch"]
        timestamp = datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")

        entry = {
            "author": author,
            "action": action_type,
            "from_branch": from_branch,
            "to_branch": to_branch,
            "timestamp": timestamp
        }

        collection.insert_one(entry)
        return jsonify({"status": "success"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/actions", methods=["GET"])
def get_actions():
    docs = collection.find().sort("_id", -1).limit(10)
    result = []

    for doc in docs:
        result.append({
            "author": doc["author"],
            "action": doc["action"],
            "from_branch": doc.get("from_branch", ""),
            "to_branch": doc["to_branch"],
            "timestamp": doc["timestamp"]
        })

    return jsonify(result)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
