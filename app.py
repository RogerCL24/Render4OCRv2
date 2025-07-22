from flask import Flask, request, jsonify
from pdf2image import convert_from_bytes
from PIL import Image
import requests
import os
import io

app = Flask(__name__)

OCR_SPACE_API_KEY = os.getenv("OCR_SPACE_API_KEY", "helloworld")

def ocr_image(img: Image.Image):
    url = "https://api.ocr.space/parse/image"
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    buffered.seek(0)

    files = {"filename": ("page.jpg", buffered, "image/jpeg")}
    payload = {
        "apikey": OCR_SPACE_API_KEY,
        "language": "spa",  # cambia a "eng" si necesitas inglés
        "isOverlayRequired": False,
        "scale": True,
        "OCREngine": 2
    }

    response = requests.post(url, data=payload, files=files)
    try:
        result = response.json()
        return result["ParsedResults"][0]["ParsedText"].strip()
    except Exception:
        return ""

def ocr_pdf_file(file):
    try:
        images = convert_from_bytes(file.read())
    except Exception as e:
        print("Error al convertir PDF a imágenes:", e)
        return "Error: El archivo no es un PDF válido o está dañado."

    full_text = ""
    for img in images:
        text = ocr_image(img)
        full_text += text + "\n--- PAGE BREAK ---\n"
    return full_text.strip()


@app.route('/ocr-header', methods=['POST'])
def ocr_header():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    full_text = ocr_pdf_file(file)
    first_line = full_text.strip().splitlines()[0] if full_text else "Error: No se pudo leer texto"
    return jsonify({
        "header_text": first_line,
        "full_text": full_text if full_text else "Error: No se pudo leer texto"
    })

@app.route('/ping')
def ping():
    return "pong"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
