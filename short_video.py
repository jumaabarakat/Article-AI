import moviepy.editor as mp
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
from openai import OpenAI
from dotenv import load_dotenv
import re


load_dotenv()

client = OpenAI(
    api_key=os.getenv('api_key')
)

def extract_video_id(url):
    pattern = r"(?:youtu\.be/|(?:www\.|m\.)?youtube\.com/(?:watch\?v=|embed/|v/|.*[?&]v=|shorts/)?)([^&\n]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_video_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        print(f"Failed to fetch transcript: {e}")
        return None  # Return None if fetching fails

def generate_summary(transcript_text):
    """Generates a summary of the transcript text using OpenAI's API."""
    prompt = f"Summarize the following text:\n{transcript_text}"
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # Fixed the engine parameter to model
            messages=[
                {"role": "system", "content": "You are an assistant that helps generate summaries."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        summary = response.choices[0].message.content.strip()  # Fixed accessing summary content
        return summary
    except Exception as e:
        raise RuntimeError(f"Failed to generate summary: {e}")

def add_subtitles(video_path, transcript, summary, output_path):
    """Overlay subtitles on the summarized video."""
    def generator(txt):
        return TextClip(txt, font='Arial', fontsize=24, color='white')
    
    # Create a list of subtitle entries [(start, end, text), ...]
    subs = [(t['start'], t['start'] + t['duration'], t['text']) for t in transcript]
    
    # Create a subtitles clip
    video_clip = VideoFileClip(video_path)
    subtitles = SubtitlesClip(subs, generator)
    
    # Add summary as a subtitle
    summary_clip = TextClip(summary, fontsize=24, color='white', bg_color='black', size=video_clip.size)
    summary_clip = summary_clip.set_duration(video_clip.duration).set_position(('center', 'bottom'))
    
    # Overlay subtitles and summary on the video
    result = mp.CompositeVideoClip([video_clip, subtitles.set_position(('center', 'bottom')), summary_clip])
    
    # Write the result to a file
    result.write_videofile(output_path, codec='libx264')

def process_video(youtube_url, start_time, end_time, output_file):
    """Download, cut, summarize, and overlay summary on the video."""
    video_id = extract_video_id(youtube_url)
    print("Extracted Video ID:", video_id)  # Debugging line
    if not video_id:
        raise ValueError("Invalid YouTube URL")

    # Download YouTube video
    yt = YouTube(youtube_url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    video_path = "/Users/mvp/Desktop/Article-AI/short_vid/short_vid.mp4"

    if not os.path.exists(video_path):
        stream.download(output_path="/Users/mvp/Desktop/Article-AI/short_vid", filename="original_video.mp4")

    # Cut the video from start_time to end_time
    video_clip = mp.VideoFileClip(video_path).subclip(start_time, end_time)
    short_video_path = os.path.join('short_vid', 'short_video.mp4')
    video_clip.write_videofile(short_video_path, codec='libx264')

    # Generate the transcript and summary
    transcript_text = get_video_transcript(video_id)
    summary = generate_summary(transcript_text)

    # Add subtitles and summary to the video
    add_subtitles(short_video_path, transcript_text, summary, output_file)

    # Remove intermediate files
    os.remove(video_path)  # You may want to keep short_video.mp4 if needed

    return output_file