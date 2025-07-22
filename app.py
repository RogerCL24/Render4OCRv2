from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError
import io, requests

app = Flask(__name__)

@app.route('/extract-text', methods=['POST'])
def extract_text():
    data = request.get_json(silent=True)
    if not data or 'pdf_url' not in data:
        return jsonify({"error": "Missing 'pdf_url' in JSON payload"}), 400

    pdf_url = data['pdf_url']
    print(f"→ Descargando PDF desde: {pdf_url}")

    try:
        response = requests.get(pdf_url)
        response.raise_for_status()

        reader = PdfReader(io.BytesIO(response.content))
        text = ""
        for i in range(min(2, len(reader.pages))):
            page = reader.pages[i]
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

        return jsonify({"text": text.strip()}), 200

    except PdfReadError as e:
        return jsonify({"error": f"PyPDF2 error: {str(e)}"}), 422
    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Extractor de texto por URL activo"}), 200
