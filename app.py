from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "OK from Flask on Render", 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    # For local dev only; Render uses gunicorn
    app.run(host="0.0.0.0", port=5000, debug=True)
