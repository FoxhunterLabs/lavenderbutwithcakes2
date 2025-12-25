from flask import Flask, jsonify
from config import APP_NAME

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "app": APP_NAME})

if __name__ == "__main__":
    app.run(debug=True)
