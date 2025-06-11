from flask import Flask, request, send_file, jsonify
import os
import fitz  # PyMuPDF
from docx import Document
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "upload"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/convert/pdf-to-word", methods=["POST"])
def convert_pdf_to_word():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = secure_filename(file.filename)
    if not filename.lower().endswith(".pdf"):
        return jsonify({"error": "Invalid file type. Upload a PDF."}), 400

    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    doc = fitz.open(input_path)
    word_doc = Document()

    for page in doc:
        text = page.get_text()
        word_doc.add_paragraph(text)

    output_filename = filename.rsplit(".", 1)[0] + ".docx"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
    word_doc.save(output_path)

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
