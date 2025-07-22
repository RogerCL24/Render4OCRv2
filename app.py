from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
import io

app = Flask(__name__)

@app.route('/extract-text', methods=['POST'])
def extract_text
    file = request.files.get("file")
    print("→ filename:", file.filename)
    print("→ content‑type:", file.mimetype)
    print("→ size bytes:", file.content_length)   # a veces es None

    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    reader = PdfReader(io.BytesIO(file.read()))
    text = ""

    for i in range(min(2, len(reader.pages))):
        text += reader.pages[i].extract_text() + "\n"

    return jsonify({"text": text.strip()}), 200

if __name__ == '__main__':
    app.run(debug=True)
