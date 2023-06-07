from flask import Flask, render_template, request
from google.cloud import translate

# Set up the Flask application
app = Flask(__name__)

# Initialize the Google Translate client
translate_client = translate.TranslationServiceClient()

# Define the translation route
@app.route('/')
def translation_form():
    return render_template('translation_form.html')

@app.route('/', methods=['POST'])
def translate_text():
    # Get the text to translate from the form
    text = request.form['text']

    # Set up the translation request
    parent = translate_client.location_path("YOUR_PROJECT_ID", "global")
    response = translate_client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": "ur",
            "target_language_code": "en",
        }
    )

    # Get the translated text from the response
    translated_text = response.translations[0].translated_text

    return render_template('translation_result.html', translated_text=translated_text)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
