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

@app.route("/webhook", methods=["GET", "POST", "HEAD"])
def github_webhook():
    if request.method != "POST":
        return jsonify({"message": "Webhook is up"}), 200

    data = request.json
    event = request.headers.get("X-GitHub-Event", "ping")

    try:
        if event == "push":
            action_type = "PUSH"
            author = data["pusher"]["name"]
            from_branch = ""
            to_branch = data["ref"].split("/")[-1]

        elif event == "pull_request":
            action_type = "PULL_REQUEST"
            author = data["pull_request"]["user"]["login"]
            from_branch = data["pull_request"]["head"]["ref"]
            to_branch = data["pull_request"]["base"]["ref"]

        else:
            return jsonify({"message": "Unhandled event type"}), 200

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
