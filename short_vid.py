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
import re

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
    
    # Ensure that the transcription has the expected structure
    if hasattr(transcription, 'text'):
        return transcription.text
    else:
        print("Transcription object does not have 'text' attribute.")
        return ""

def summarize_text(transcription):
    """Generates a summary and returns important parts with timestamps."""
    prompt = f"Summarize this text and highlight the key moments with timestamps: {transcription}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an assistant that summarizes text and extracts key moments with timestamps."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )

        # Print the entire API response for debugging
        print("API Response:", response)

        # Access the content in the response properly
        if response.choices and len(response.choices) > 0:
            return response.choices[0].message.content
        else:
            print("No valid choices found in the response.")
            return {}

    except Exception as e:
        print(f"Error during summarization: {e}")
        return {}

def extract_summary_and_timestamps(response_content):
    try:
        # Check the type of response for debugging
        print("Type of response in extract_summary_and_timestamps:", type(response_content))
        
        # Print the raw content for debugging
        print("Response Content:", response_content)  
        
        # Split the content into summary and timestamps sections
        summary_section = response_content.split("**Key Moments with Timestamps:**")[0].strip()
        timestamps_section = response_content.split("**Key Moments with Timestamps:**")[1].strip() if "**Key Moments with Timestamps:**" in response_content else ""

        # Extract individual timestamps using regex
        timestamp_matches = re.findall(r'\*\*(\d+:\d+)\*\*', timestamps_section)
        print(f"Extracted timestamps: {timestamp_matches}")

        # Ensure we have pairs of timestamps
        timestamps = [(timestamp_matches[i], timestamp_matches[i + 1]) for i in range(0, len(timestamp_matches), 2) if i + 1 < len(timestamp_matches)]

        return summary_section, timestamps

    except (KeyError, IndexError) as e:
        print(f"Error extracting summary or timestamps: {e}")
        return None, None

def extract_relevant_clips(video_path, timestamps):
    """Extracts relevant clips from the video based on provided timestamps."""
    
    video = VideoFileClip(video_path)
    clips = []

    for timestamp in timestamps:
        start_time = convert_to_seconds(timestamp[0])
        end_time = start_time + 15  # Assuming each key moment is 15 seconds for demo purposes
        # Extract subclip using the provided start and end times
        subclip = video.subclip(start_time, end_time)
        clips.append(subclip)

    # Concatenate all extracted clips to form the final video
    final_clip = concatenate_videoclips(clips)
    
    return final_clip

def add_subtitles_to_video(video, summarized_text):
    """Adds subtitles (the summarized text) to the video without ImageMagick."""
    
    # Create a text image using PIL
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        font = ImageFont.load_default()

    text_image = Image.new("RGB", (video.w, 50), color=(0, 0, 0))
    draw = ImageDraw.Draw(text_image)
    draw.text((10, 10), summarized_text, font=font, fill=(255, 255, 255))
    
    # Convert PIL image to numpy array
    text_image_np = np.array(text_image)
    
    # Create a text clip from the numpy array
    subtitle_clip = ImageClip(text_image_np, duration=video.duration)
    subtitle_clip = subtitle_clip.set_position(('center', 'bottom')).set_start(0)
    
    # Overlay the subtitle clip onto the video
    final_video = CompositeVideoClip([video, subtitle_clip])
    
    return final_video
def convert_to_seconds(time_str):
    """Helper function to convert 'MM:SS' string into total seconds."""
    try:
        minutes, seconds = map(int, time_str.split(":"))
        return minutes * 60 + seconds
    except ValueError:
        print(f"Invalid time format: {time_str}")
        return 0

def generate_summary(video_path):
    """Handles the complete process: extract, summarize, and add subtitles."""
    
    # Step 1: Extract transcription from video
    transcription_text = extract_audio_and_transcribe(video_path)
    if not transcription_text:
        print("Failed to extract transcription.")
        return

    # Step 2: Summarize transcription and get key moments with timestamps
    summarized_data = summarize_text(transcription_text)
    
    # Check the summarized data for debugging
    print("Summarized Data:", summarized_data)  # Print the entire summarized data
    
    if not summarized_data:
        print("Summarization failed or returned empty data.")
        return

    # Extract summary and timestamps using the new function
    summary, timestamps = extract_summary_and_timestamps(summarized_data)
    
    if not summary or not timestamps:
        print("Failed to extract summary or timestamps from the response.")
        return None

    print("Summary generation successful.")  # Debugging success point

    # Step 4: Extract relevant video clips based on timestamps
    final_clip = extract_relevant_clips(video_path, timestamps)
    
    # Step 5: Add summarized text as subtitles to the shortened video
    final_video_with_subtitles = add_subtitles_to_video(final_clip, summary)
    
    # Step 6: Save the final video
    output_path = "short_summary_with_subtitles.mp4"
    final_video_with_subtitles.write_videofile(output_path, codec="libx264", threads=4)
    
    return output_path
