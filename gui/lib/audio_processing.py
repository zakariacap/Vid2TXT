import os
import subprocess
from pydub import AudioSegment
import speech_recognition as sr

def extract_audio_from_video(video_path: str, output_path: str = "temp_audio.wav"):
    """
    Extract audio from video file using FFmpeg
    Supports multiple video formats
    """
    try:
        subprocess.run([
            'ffmpeg', 
            '-i', video_path,  # Input video file
            '-vn',             # Ignore video
            '-acodec', 'pcm_s16le',  # Audio codec
            '-ar', '44100',    # Audio sample rate
            '-ac', '1',        # Mono audio
            output_path        # Output audio file
        ], check=True)
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Error extracting audio: {e}")
        return None

def process_audio_file(file_path: str, language: str = "en"):
    """
    Process the audio file to perform speech recognition.
    Supports multiple languages and video formats.
    """
    # Check if input is a video file
    video_extensions = ['.mkv', '.mp4', '.avi', '.mov']
    file_ext = os.path.splitext(file_path)[1].lower()
    
    # If it's a video file, extract audio first
    if file_ext in video_extensions:
        audio_file = extract_audio_from_video(file_path)
        if not audio_file:
            return "Could not extract audio from video"
    else:
        audio_file = file_path

    try:
        # Load the audio file
        audio = AudioSegment.from_file(audio_file)

        # Convert the audio to WAV format for processing
        wav_file_path = "temp_audio.wav"
        audio.export(wav_file_path, format="wav")

        # Perform speech recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_file_path) as source:
            audio_data = recognizer.record(source)
            try:
                # Recognize speech using the specified language
                text = recognizer.recognize_google(audio_data, language=language)
            except sr.UnknownValueError:
                text = "Speech recognition could not understand the audio."
            except sr.RequestError as e:
                text = f"Could not request results from the speech recognition service; {e}"

        # Clean up the temporary WAV files
        os.remove(wav_file_path)
        if file_ext in video_extensions:
            os.remove(audio_file)

        return text

    except Exception as e:
        return f"Error processing audio: {str(e)}"