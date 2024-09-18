import whisperx
import subprocess

def convert_to_wav(input_file, output_file):
    """Convert an audio file to wav format using ffmpeg."""
    print(f"Starting ffmpeg conversion from {input_file} to {output_file}")
    try:
        command = ["ffmpeg", "-i", input_file, output_file]
        subprocess.run(command, check=True)
        print(f"Conversion completed successfully.")
    except Exception as e:
        print(f"Error during conversion: {e}")

def transcribe_audio(file_path):
    """Transcribe the audio file using WhisperX."""
    device = "cpu"
    
    print("Loading model...")
    try:
        model = whisperx.load_model("small", device, compute_type="float32")
        print("Model loaded")
    except Exception as e:
        print(f"Error during model loading: {e}")
        raise e

    # Load audio and transcribe
    try:
        audio = whisperx.load_audio(file_path)
        print(f"Transcribing {file_path}")
        result = model.transcribe(audio)
        print(f"Transcription completed.")
        return result['segments']
    except Exception as e:
        print(f"Error during transcription: {e}")
        raise e


