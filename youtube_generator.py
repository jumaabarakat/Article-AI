import re
from youtube_transcript_api import YouTubeTranscriptApi
import openai
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client with API key from .env
client = OpenAI(
    api_key=os.getenv('api_key')
)

def extract_video_id(url):
    """Extracts the video ID from a YouTube URL."""
    regex = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.match(regex, url)
    if match:
        return match.group(1)
    else:
        return None

def get_video_transcript(video_id, language):
    """Fetches the transcript of a YouTube video."""
    try:
        # Attempt to get the transcript in the specified language
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
    except Exception:
        # If it fails, try to get the auto-generated English transcript
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        except Exception as e:
            raise Exception(f"Could not retrieve transcript: {e}")

    transcript_text = " ".join([t['text'] for t in transcript])
    return transcript_text

def generate_summary(transcript_text, language, type_of_summary):
    """Generates a summary using the OpenAI API."""
    if language == "Arabic":
        prompt_language = "in Arabic"
    else:
        prompt_language = "in English"
    
    summary_type = "detailed" if type_of_summary == "Detailed" else "short"
    
    prompt = f"Generate a {summary_type} summary for the following transcript {prompt_language}:\n{transcript_text}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an assistant that helps write summaries."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500 if type_of_summary == "Detailed" else 200,
            temperature=0.7,
        )
        # Access the content from the response correctly
        summary = response.choices[0].message.content.strip()  # Updated line
        return summary
    except Exception as e:
        raise Exception(f"Error generating summary: {e}")