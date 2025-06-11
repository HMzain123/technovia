from flask import Blueprint, request, send_file, jsonify
from pdf2docx import Converter
import os
import uuid

pdf_to_word_route = Blueprint('pdf_to_word_route', __name__)

UPLOAD_FOLDER = 'upload'
OUTPUT_FOLDER = 'outputs'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@pdf_to_word_route.route('/convert/pdf-to-word', methods=['POST'])
def convert_pdf_to_word():
    try:
        file = request.files.get('file')
        if not file:
            return jsonify({'error': 'No file uploaded'}), 400

        # Generate unique filenames
        input_filename = f"{uuid.uuid4().hex}.pdf"
        input_path = os.path.join(UPLOAD_FOLDER, input_filename)
        output_filename = input_filename.replace(".pdf", ".docx")
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        # Save the uploaded PDF
        file.save(input_path)

        # Convert PDF to DOCX
        cv = Converter(input_path)
        cv.convert(output_path, start=0, end=None)
        cv.close()

        # Return the converted DOCX file
        return send_file(output_path,
                         as_attachment=True,
                         download_name='converted.docx',
                         mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

    except Exception as e:
        print(f"Conversion failed: {str(e)}")
        return jsonify({'error': 'Conversion failed or server error'}), 500
