from flask import Flask, render_template, request
from transformers import MarianMTModel, MarianTokenizer

app = Flask(__name__)

model_name = "Helsinki-NLP/opus-mt-en-ur"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

@app.route('/', methods=['GET', 'POST'])
def translate():
    if request.method == 'POST':
        text = request.form['text']
        inputs = tokenizer(text, return_tensors="pt")
        translated = model.generate(**inputs, max_length=50)
        translated_text = tokenizer.batch_decode(translated, skip_special_tokens=True)[0]
        return render_template('index.html', translated_text=translated_text)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
