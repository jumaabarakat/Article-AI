from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, ImageClip
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
from PIL import Image, ImageDraw, ImageFont
import numpy as np


load_dotenv()


client = OpenAI(
    api_key=os.getenv('api_key')
)
def extract_audio_and_transcribe(video_path):
    """Extract the audio from the video and transcribe it using OpenAI's Whisper API."""
    
    # Step 1: Extract audio from the video
    ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
    audio_output_path = "temp_audio.mp3"
    subprocess.run([ffmpeg_exe, '-i', video_path, '-q:a', '0', '-map', 'a', audio_output_path])

    # Step 2: Transcribe audio using OpenAI Whisper
    with open(audio_output_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
    
    # Access the transcription text using the attribute `text`
    transcribed_text = transcription.text  # Access the 'text' attribute directly
    return transcribed_text


def summarize_text(transcription):
    """Generates a summary and returns important parts with timestamps."""
    prompt = f"Summarize this text and highlight the key moments with timestamps: {transcription}"
    
    response = client.chat.completions.create(
        model="gpt-4-mini",
        messages=[
            {"role": "system", "content": "You are an assistant that summarizes text and extracts key moments with timestamps."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7
    )

    # The output needs to include a summary along with timestamps, which GPT will return.
    return response.choices[0].message.content.strip()

def extract_relevant_clips(video_path, timestamps):
    """Extracts relevant clips from the video based on provided timestamps."""
    
    video = VideoFileClip(video_path)
    clips = []

    for start_time, end_time in timestamps:
        # Extract subclip using the provided start and end times
        subclip = video.subclip(start_time, end_time)
        clips.append(subclip)

    # Concatenate all extracted clips to form the final video
    final_clip = concatenate_videoclips(clips)
    
    return final_clip

def add_subtitles_to_video(video, summarized_text):
    """Adds subtitles (the summarized text) to the video without ImageMagick."""
    
    # Create a text clip for the summarized text
    subtitle_clip = TextClip(summarized_text, fontsize=24, color='white', size=video.size)
    
    # Set the duration of the subtitle and position it at the bottom
    subtitle_clip = subtitle_clip.set_duration(video.duration).set_position(('center', 'bottom')).set_start(0)
    
    # Overlay the subtitle clip onto the video
    final_video = CompositeVideoClip([video, subtitle_clip])
    
    return final_video

def generate_summary(video_path):
    """Handles the complete process: extract, summarize, and add subtitles."""
    
    # Step 1: Extract transcription from video
    transcription_text = extract_audio_and_transcribe(video_path)
    
    # Step 2: Summarize transcription and get key moments with timestamps
    summarized_data = summarize_text(transcription_text)
    
    # Parse timestamps and summarized text
    # Assume the format returned from GPT is something like: "Key moments: 0:00-0:15, 1:10-1:30. Summary: ..."
    summary, timestamps = parse_summary_and_timestamps(summarized_data)
    
    # Step 3: Extract relevant video clips based on timestamps
    final_clip = extract_relevant_clips(video_path, timestamps)
    
    # Step 4: Add summarized text as subtitles to the shortened video
    final_video_with_subtitles = add_subtitles_to_video(final_clip, summary)
    
    # Step 5: Save the final video
    output_path = "short_summary_with_subtitles.mp4"
    final_video_with_subtitles.write_videofile(output_path, codec="libx264", threads=4)
    
    return output_path

def parse_summary_and_timestamps(summarized_data):
    """Helper function to extract summary text and timestamp information."""
    # Example of parsing logic, depending on GPT output format
    summary = summarized_data.split("Summary:")[1].strip()
    
    timestamps_text = summarized_data.split("Key moments:")[1].split("Summary:")[0].strip()
    timestamps = []
    
    # Convert timestamps like "0:00-0:15" into (start_time, end_time) tuples
    for time_range in timestamps_text.split(","):
        start_time, end_time = time_range.split("-")
        timestamps.append((convert_to_seconds(start_time), convert_to_seconds(end_time)))
    
    return summary, timestamps

def convert_to_seconds(time_str):
    """Helper function to convert 'MM:SS' string into total seconds."""
    minutes, seconds = map(int, time_str.split(":"))
    return minutes * 60 + seconds



















































































