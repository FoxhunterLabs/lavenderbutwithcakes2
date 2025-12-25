import os
from flask import Flask, jsonify

from app.core.config import APP_NAME

def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/health")
    def health():
        return jsonify({
            "status": "healthy",
            "app": APP_NAME
        })

    return app

if __name__ == "__main__":
    app = create_app()
    print(f"{APP_NAME} running on http://localhost:5000")
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "5000")),
        debug=True,
    )
