from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)


CORS(app, resources={r"/*": {"origins": "*"}})


MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.github_webhook
collection = db.actions


@app.route("/webhook", methods=["GET", "POST", "HEAD"])
def github_webhook():
    if request.method != "POST":
        return jsonify({"message": "Webhook is up"}), 200

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
    try:
        docs = collection.find().sort("_id", -1).limit(10)
        result = []
        for doc in docs:
            result.append({
                "author": doc.get("author", ""),
                "action": doc.get("action", ""),
                "from_branch": doc.get("from_branch", ""),
                "to_branch": doc.get("to_branch", ""),
                "timestamp": doc.get("timestamp", "")
            })
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
