from flask import Flask, jsonify
from config import APP_NAME
from db import init_db

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "app": APP_NAME})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
