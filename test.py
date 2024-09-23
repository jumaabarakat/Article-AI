import os
import re
from short_video import (
    extract_video_id,
    get_video_transcript,
    generate_summary,
    add_subtitles,
    process_video
)
# correct
def test_extract_video_id():
    print("Testing extract_video_id...")
    urls = [
        "https://youtu.be/3k89FMJhZ00?si=lVvQ9YhiQjjwWngR",  # Valid URL
        "https://youtu.be/3k89FMJhZ00?si=lVvQ9YhiQjjwWngR",                 # Shortened URL
        "https://www.youtube.com/3k89FMJhZ00?si=lVvQ9YhiQjjwWngR",    # Embed URL
        "invalid_url"                                    # Invalid URL
    ]
    for url in urls:
        video_id = extract_video_id(url)
        print(f"URL: {url}\nExtracted Video ID: {video_id}\n")
# correct
def test_get_video_transcript():
    print("Testing get_video_transcript...")
    video_id = "3k89FMJhZ00?si=lVvQ9YhiQjjwWngR"  # Use a valid video ID for testing
    transcript = get_video_transcript(video_id)
    print("Transcript:", transcript)
# correct
def test_generate_summary():
    print("Testing generate_summary...")
    transcript_text = "This is a sample transcript text for summarization."
    try:
        summary = generate_summary(transcript_text)
        print("Summary:", summary)
    except Exception as e:
        print("Error generating summary:", e)

def test_add_subtitles():
    print("Testing add_subtitles...")
    video_path = "/Users/mvp/Desktop/Article-AI/short_vid/short_vid.mp4"  # Ensure this video exists for testing
    transcript = [{"start": 0, "duration": 5, "text": "Hello, this is a test."}]
    summary = "This is a summary of the video."
    output_path = "output_video.mp4"
    try:
        add_subtitles(video_path, transcript, summary, output_path)
        print(f"Subtitled video saved as: {output_path}")
    except Exception as e:
        print("Error adding subtitles:", e)

def test_process_video():
    print("Testing process_video...")
    youtube_url = "https://www.youtube.com/DLEL6i0YmkY?si=T3la29FeN5LmBZxj"  # Replace with a valid URL
    start_time = 0  # Start time in seconds
    end_time = 10   # End time in seconds
    output_file = "final_summary.mp4"
    try:
        processed_video = process_video(youtube_url, start_time, end_time, output_file)
        print(f"Processed video saved as: {processed_video}")
    except Exception as e:
        print("Error processing video:", e)

if __name__ == "__main__":
    test_extract_video_id()
    test_get_video_transcript()
    test_generate_summary()
    test_add_subtitles()
    test_process_video()
