from flask import Flask, render_template, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os
# import pytesseract
# pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Mrunal\Tesseract_OCR\tesseract.exe"
from gtts import gTTS


import pytesseract

# If on Windows, you can leave the path, but on cloud servers, it will default to system path
try:
    if os.name == 'nt':  # For Windows, you can still specify the path
        pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Mrunal\Tesseract_OCR\tesseract.exe"
    else:  # For Linux environments, let Tesseract be found on the system path
        pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # typical path on Linux servers
except Exception as e:
    print(f"Error configuring Tesseract: {e}")



# Set up Tesseract path if needed (example for Windows)
# pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')
# def hello_world():
#     return 'Hello, World!'


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

        # Extract text using pytesseract
        try:
            from PIL import Image

# Open the image with PIL to make sure it's a valid image
            image = Image.open(filepath)

# Now pass this image to Tesseract
            extracted_text = pytesseract.image_to_string(image, lang=language)
            
            if not extracted_text.strip():
                print("No text extracted! Image might be too poor quality.")
        except Exception as e:
            print(f"Error during OCR: {e}")
            extracted_text = ''

        print(f"Extracted Text: {extracted_text}")

        # Convert text to speech
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
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
