from flask import Flask, request, jsonify
import os
from datetime import datetime
import json

app = Flask(__name__)

# Directory where files will be saved
SAVE_DIR = "saved"
os.makedirs(SAVE_DIR, exist_ok=True)


@app.route("/", methods=["GET"])
def index():
    return "OK from Flask on Render", 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/save", methods=["POST"])
def save_text():
    """
    Accepts any body (JSON, XML, plain text) and saves it to a file.
    """
    # Raw body as text
    raw_body = request.data.decode("utf-8", errors="replace")

    if not raw_body:
        return jsonify({"error": "No data received"}), 400

    # Optional: pretty-print JSON if content-type is JSON
    content_type = request.headers.get("Content-Type", "").lower()
    to_write = raw_body

    if "application/json" in content_type:
        try:
            parsed = json.loads(raw_body)
            to_write = json.dumps(parsed, indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            # If JSON is invalid, just save the raw body
            pass

    # Timestamp-based filename
    filename = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}.txt"
    filepath = os.path.join(SAVE_DIR, filename)

    # Save to file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(to_write)

    return jsonify({
        "status": "saved",
        "file": filename,
        "content_type": content_type,
    }), 200


if __name__ == "__main__":
    # Local dev only; Render uses gunicorn
    app.run(host="0.0.0.0", port=5000, debug=True)
