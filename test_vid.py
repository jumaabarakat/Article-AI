# test_vid.py
from short_vid import (
    extract_audio_and_transcribe,
    summarize_text,
    add_subtitles_to_video,
    generate_summary
)

def test_extract_audio_and_transcribe(video_path):
    print("Testing audio extraction and transcription...")
    try:
        transcription = extract_audio_and_transcribe(video_path)
        print("Transcription successful:")
        print(transcription)
    except Exception as e:
        print(f"Error during transcription: {e}")

def test_summarize_text(text):
    print("Testing text summarization...")
    try:
        summary = summarize_text(text)
        print("Summarization successful:")
        print(summary)
    except Exception as e:
        print(f"Error during summarization: {e}")

def test_add_subtitles_to_video(video_path, summarized_text):
    print("Testing adding subtitles to video...")
    try:
        output_path = add_subtitles_to_video(video_path, summarized_text)
        print(f"Subtitles added successfully. Output video path: {output_path}")
    except Exception as e:
        print(f"Error during adding subtitles: {e}")

def test_generate_summary(video_path):
    print("Testing full summary generation...")
    try:
        output_path = generate_summary(video_path)
        print(f"Summary generation successful. Output video path: {output_path}")
    except Exception as e:
        print(f"Error during summary generation: {e}")

if __name__ == "__main__":
    # Change 'path_to_your_video.mp4' to the actual path of your video file
    video_path = '/Users/mvp/Desktop/videoplayback (1) (1).mp4'
    
    # Test functions individually
    test_extract_audio_and_transcribe(video_path)
    
    # Use some sample text for summarization
    # sample_text = "This is a test text for summarization."
    # test_summarize_text(sample_text)
    
    # # Test adding subtitles (provide a dummy summary for this test)
    # dummy_summary = "This is a dummy summary for testing."
    # test_add_subtitles_to_video(video_path, dummy_summary)
    
    # # Test full summary generation
    # test_generate_summary(video_path)
