from flask import Flask, render_template, request, send_file
from transformers import MarianMTModel, MarianTokenizer
import os
import pytesseract
from pdf2image import convert_from_path
from urduhack.tokenization import sentence_tokenizer
import shutil
from werkzeug.utils import secure_filename
import zipfile
from config import model_name, poppler_path, tesseract_cmd, secret_key

app = Flask(__name__, static_url_path='/static')
app.secret_key = secret_key
app.config['TEMPLATES_AUTO_RELOAD'] = True
pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

model_name = "checkpoint-102000"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

def pdf_to_image(filepath):
    images = convert_from_path(filepath, poppler_path=poppler_path)
    return images

def ocr_images(image_path, lang):
    text = pytesseract.image_to_string(image_path, lang=lang)
    return text

def process_pdf(filepath):
    ocr_content = []
    image_list = pdf_to_image(filepath)
    for image in image_list:
        content = ocr_images(image, lang="eng")
        content = content.strip()
        ocr_content.append(content)
    final = "\n".join(ocr_content)
    return final.strip()

def translate_sentences(sentences):
    translations = []
    for sentence in sentences:
        inputs = tokenizer(sentence, return_tensors="pt")
        translated = model.generate(**inputs, max_length=50)
        translated_text = tokenizer.batch_decode(translated, skip_special_tokens=True)[0]
        translations.append(translated_text)
    return translations

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    if request.method == 'POST':
        text = request.form['text']
        inputs = tokenizer(text, return_tensors="pt")
        translated = model.generate(**inputs, max_length=50)
        translated_text = tokenizer.batch_decode(translated, skip_special_tokens=True)[0]
        return translated_text

@app.route('/document', methods=['GET', 'POST'])
def document_translation():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_extension = os.path.splitext(uploaded_file.filename)[1].lower()
            print(file_extension)
            if file_extension == '.pdf':
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(uploaded_file.filename))
                uploaded_file.save(file_path)
                final_data = process_pdf(file_path)
                sentences = sentence_tokenizer(final_data)
                translations = translate_sentences(sentences)
                translated_text = '\n'.join(translations)
                translated_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"Translated_{os.path.splitext(uploaded_file.filename)[0]}.txt")
                with open(translated_file_path, 'w', encoding='utf-8') as f:
                    f.write(translated_text)

                return send_file(translated_file_path, as_attachment=True, mimetype='text/plain')
            elif file_extension == '.zip':
                # Create a folder to store extracted files
                extract_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'extracted')
                os.makedirs(extract_folder, exist_ok=True)

                # Extract all PDF files from the ZIP
                with zipfile.ZipFile(uploaded_file, 'r') as zip_file:
                    zip_file.extractall(extract_folder)

                # Translate each extracted PDF file
                translations_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'translated', f"Translated_{os.path.splitext(uploaded_file.filename)[0]}")
                os.makedirs(translations_folder, exist_ok=True)

                for filename in os.listdir(extract_folder):
                    if filename.lower().endswith('.pdf'):
                        pdf_path = os.path.join(extract_folder, filename)
                        final_data = process_pdf(pdf_path)
                        sentences = sentence_tokenizer(final_data)
                        translations = translate_sentences(sentences)
                        translated_text = '\n'.join(translations)
                        translated_file_path = os.path.join(translations_folder, f"{os.path.splitext(filename)[0]}_translated.txt")
                        with open(translated_file_path, 'w', encoding='utf-8') as f:
                            f.write(translated_text)

                # Create a ZIP file of the translated files
                translated_zip_path = os.path.join(app.config['UPLOAD_FOLDER'], f"Translated_{os.path.splitext(uploaded_file.filename)[0]}_files.zip")
                with zipfile.ZipFile(translated_zip_path, 'w') as zip_file:
                    for filename in os.listdir(translations_folder):
                        zip_file.write(os.path.join(translations_folder, filename), filename)

                return send_file(translated_zip_path, as_attachment=True, mimetype='application/zip')

        return "No file uploaded"

    return render_template('document.html')

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')  # Specify the folder to save uploaded files
    app.run(debug=True)