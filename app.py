from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError
import io

app = Flask(__name__)

@app.route('/extract-text', methods=['POST'])
def extract_text():
    file = request.files.get('file')
    
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    try:
        print("→ filename:", file.filename)
        print("→ content-type:", file.mimetype)
        print("→ file size (bytes):", file.content_length)

        pdf_bytes = file.read()
        reader = PdfReader(io.BytesIO(pdf_bytes))

        text = ""
        for i in range(min(2, len(reader.pages))):
            page = reader.pages[i]
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

        return jsonify({
            "text": text.strip()
        })

    except PdfReadError as e:
        return jsonify({"error": f"PyPDF2 error: {str(e)}"}), 422

    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Extractor de texto activo"}), 200

if __name__ == '__main__':
    app.run(debug=True)
