from flask import Flask, render_template, request
from transformers import MarianMTModel, MarianTokenizer

app = Flask(__name__, static_url_path='/static')
app.config['TEMPLATES_AUTO_RELOAD'] = True

model_name = "Helsinki-NLP/opus-mt-en-ur"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

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

@app.route('/document', methods=['GET'])
def document_translation():
    return render_template('document.html')

if __name__ == '__main__':
    app.run(debug=True)
