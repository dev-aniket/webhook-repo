from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # allow all for now

MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.github_webhook
collection = db.actions

@app.route("/webhook", methods=["POST"])
def github_webhook():
    try:
        data = request.json
        entry = {
            "author": data["author"],
            "action": data["action"],
            "from_branch": data.get("from_branch", ""),
            "to_branch": data["to_branch"],
            "timestamp": datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")
        }
        collection.insert_one(entry)
        return jsonify({"status": "success"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/actions", methods=["GET"])
def get_actions():
    try:
        result = list(collection.find({}, {"_id": 0}).sort("_id", -1).limit(10))
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
