from flask import Flask, jsonify
from config import APP_NAME
from db import init_db

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "app": APP_NAME})

if __name__ == "__main__":
    init_db()
    from connectors.registry import ensure_default_connectors
    ensure_default_connectors()
    app.run(debug=True)
