from flask import Flask, jsonify
from config import APP_NAME
from db import init_db
from connectors.registry import ensure_default_connectors
from api.routes import api
from ui.routes import ui

app = Flask(__name__)
app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(ui, url_prefix="/ui")


@app.route("/health")
def health():
    return jsonify({"status": "healthy", "app": APP_NAME})


if __name__ == "__main__":
    init_db()
    ensure_default_connectors()
    app.run(host="0.0.0.0", port=5000, debug=True)
