from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip
import speech_recognition as sr
import openai
import os
from openai import OpenAI
from dotenv import load_dotenv
import moviepy.editor as mp
from moviepy.video.tools.subtitles import SubtitlesClip
import whisper 
import imageio_ffmpeg as ffmpeg
from pydub import AudioSegment
import subprocess


load_dotenv()

client = OpenAI(
    api_key=os.getenv('api_key')
)

def extract_audio_and_transcribe(video_path):
    """Extract audio from the video and return transcription as text using Whisper."""
    
    # Generate a temporary audio file path
    audio_path = "temp_audio.mp3"
    print("Just above ffmpeg")
    # Use ffmpeg command from imageio-ffmpeg to extract audio
    ffmpeg_path = ffmpeg.get_ffmpeg_exe()
    command = [ffmpeg_path, '-i', video_path, '-q:a', '0', '-map', 'a', audio_path]
    
    subprocess.run(command, check=True)

    # Load Whisper model and transcribe audio
    model = whisper.load_model("base")  # Load Whisper model
    transcription = model.transcribe(audio_path)  # Transcribe MP3 directly
    
    os.remove(audio_path)  # Clean up temporary file
    return transcription['text']


def add_subtitles_to_video(video_path, summarized_text):
    """Adds subtitles (the summarized text) to the video."""
    video = mp.VideoFileClip(video_path)
    
    # Subtitles timing (adjust timing logic based on length of summary)
    subtitles_list = [(0, 5, summarized_text)]  # Example: Show subtitles from second 0 to 5
    subtitles = SubtitlesClip(subtitles_list, method='caption')
    
    # Overlay subtitles onto the video
    final_video = mp.CompositeVideoClip([video, subtitles.set_position(('center', 'bottom'))])
    output_path = "short_summary_with_subtitles.mp4"
    final_video.write_videofile(output_path, codec="libx264")
    
    return output_path


def summarize_text(text):
    """Generates a summary of the text using OpenAI's GPT API."""
    prompt=f"Summarize this text: {text}"
    response = client.chat.completions.create(
        engine="gpt-4o-mini",
        messages=[
                {"role": "system", "content": "You are an assistant that helps summarizing text."},
                {"role": "user", "content": prompt}
            ],
        max_tokens=150,
        temperature= 0.7
    )

    return response['choices'][0]['message']['content'].strip()

def generate_summary(video_path):
    """Handles the complete process: extract, summarize, and add subtitles."""
    # Step 1: Extract transcription from video
    transcription_text = extract_audio_and_transcribe(video_path)
    
    # Step 2: Summarize transcription using OpenAI GPT
    summarized_text = summarize_text(transcription_text)
    
    # Step 3: Add summarized text as subtitles to the video
    output_video_path = add_subtitles_to_video(video_path, summarized_text)
    
    return output_video_path