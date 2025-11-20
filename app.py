from flask import Flask, request, jsonify
import os
from datetime import datetime
import json

app = Flask(__name__)

# Directory where files will be saved
SAVE_DIR = "saved"
os.makedirs(SAVE_DIR, exist_ok=True)


@app.route("/save", methods=["POST"])
def save_text():
    """
    Accepts any body (JSON, XML, plain text) and saves it to a file.
    Optional ways to influence behavior:
    - Query param ?filename=mytest.txt
    - For JSON, you can send {"data": "..."} or any JSON; we'll dump it to the file.
    """

    # Raw body as bytes, decode to string
    raw_body = request.data.decode("utf-8", errors="replace")

    if not raw_body:
        return jsonify({"error": "No data received"}), 400

    # Optional: custom filename via query parameter
    custom_filename = request.args.get("filename")

    if custom_filename:
        # Very basic sanitization: no path separators
        custom_filename = os.path.basename(custom_filename)
        filename = custom_filename
    else:
        # Generate filename based on timestamp
        filename = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}.txt"

    filepath = os.path.join(SAVE_DIR, filename)

    # If content-type is JSON, pretty-print it before saving
    content_type = request.headers.get("Content-Type", "")
    to_write = raw_body

    if "application/json" in content_type.lower():
        try:
            parsed = json.loads(raw_body)
            to_write = json.dumps(parsed, indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            # If JSON is invalid, just save the raw body
            pass

    # Save to file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(to_write)

    return jsonify({
        "status": "saved",
        "file": filename,
        "content_type": content_type
    }), 200


if __name__ == "__main__":
    # For local testing
    app.run(host="0.0.0.0", port=5000)
