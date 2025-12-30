from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import os

app = Flask(__name__)

MONGO_URI = os.environ.get("MONGODB_URI", "mongodb://mongodb:27017")
client = MongoClient(MONGO_URI)
db = client.flask_db
collection = db.data

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/data", methods=["POST"])
def insert_data():
    data = request.json
    collection.insert_one(data)
    return jsonify({"message": "Data inserted"}), 201

@app.route("/data", methods=["GET"])
def get_data():
    data = list(collection.find({}, {"_id": 0}))
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
