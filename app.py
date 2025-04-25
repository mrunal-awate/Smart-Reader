from flask import Flask, render_template, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os
from gtts import gTTS
import easyocr  # Import EasyOCR

# Set up the EasyOCR Reader for specific languages
reader = easyocr.Reader(['en', 'hi', 'mr'])  # Add any other languages as needed

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    language = request.form['language']

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Check if file exists
        if os.path.exists(filepath):
            print(f"File saved at: {filepath}")

        # Extract text using EasyOCR
        try:
            # Read the image using EasyOCR
            result = reader.readtext(filepath)

            # Extract text from the OCR result
            extracted_text = " ".join([text[1] for text in result])
            
            if not extracted_text.strip():
                print("No text extracted! Image might be too poor quality.")
        except Exception as e:
            print(f"Error during OCR: {e}")
            extracted_text = ''

        print(f"Extracted Text: {extracted_text}")

        # Convert text to speech
        if not extracted_text.strip():
            return "No text extracted from the image.", 400

        tts = gTTS(text=extracted_text, lang='hi' if language == 'hin' else 'mr' if language == 'mar' else 'en')

        audio_path = os.path.join(app.config['OUTPUT_FOLDER'], 'spoken.mp3')
        tts.save(audio_path)

        return jsonify({
            'text': extracted_text,
            'audio_url': '/output/spoken.mp3'
        })

    return 'No file uploaded', 400


@app.route('/output/<filename>')
def serve_audio(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
