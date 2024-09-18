from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from transcriber import transcribe_audio, convert_to_wav

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Global variable to track progress
progress = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    global progress
    progress = 0
    if 'file' not in request.files:
        print("No file part in the request.")
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        print("No selected file.")
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    print(f"File received: {file.filename}")
    file.save(file_path)

    if file.filename.endswith('.m4a'):
        wav_path = file_path.replace('.m4a', '.wav')
        print(f"Converting {file_path} to {wav_path}")
        convert_to_wav(file_path, wav_path)
        file_path = wav_path

    try:
        # Start transcription and track progress
        print("Starting transcription...")
        subtitles = transcribe_audio(file_path)
        progress = 100  # Mark progress as completed
        print("Transcription completed.")
        return jsonify(subtitles)
    except Exception as e:
        progress = -1  # Error occurred
        print(f"Error during transcription: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/progress')
def get_progress():
    """Route to get current progress."""
    return jsonify({"progress": progress})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)

