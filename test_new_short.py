from short_vid import (
    extract_audio_and_transcribe,
    summarize_text,
    extract_relevant_clips,
    add_subtitles_to_video,
    generate_summary
)

def test_extract_audio_and_transcribe(video_path):
    print("Testing audio extraction and transcription...")
    try:
        transcription = extract_audio_and_transcribe(video_path)
        print("Transcription successful:")
        print(transcription)  # Print the transcription to debug

        # Access the 'text' key if transcription is a dictionary
        if isinstance(transcription, dict) and 'text' in transcription:
            return transcription['text']
        else:
            print("Transcription does not contain 'text'.")
            return None
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None

def test_summarize_text(transcription):
    print("Testing text summarization...")
    try:
        if transcription is not None:
            print(f"Transcription to summarize: {transcription}")
            summary = summarize_text(transcription)
            if summary:
                print("Summarization successful:")
                print(summary)
                return summary
            else:
                print("Received an empty summary.")
                return None
        else:
            print("No transcription provided for summarization.")
            return None
    except Exception as e:
        print(f"Error during summarization: {e}")
        return None

# def test_parse_summary_and_timestamps(summarized_data):
#     print("Testing parsing of summary and timestamps...")
#     try:
#         summary, timestamps = parse_summary_and_timestamps(summarized_data)
#         print("Parsed Summary:", summary)
#         print("Parsed Timestamps:", timestamps)
#         return summary, timestamps
#     except Exception as e:
#         print(f"Error during parsing: {e}")
#         return None, None

def test_extract_relevant_clips(video_path, timestamps):
    print("Testing extraction of relevant clips...")
    try:
        final_clip = extract_relevant_clips(video_path, timestamps)
        print("Clips extracted successfully.")
        return final_clip
    except Exception as e:
        print(f"Error during clip extraction: {e}")
        return None

def test_add_subtitles_to_video(video, summarized_text):
    print("Testing adding subtitles to video...")
    try:
        final_video = add_subtitles_to_video(video, summarized_text)  # Pass video object
        output_path = "output_with_subtitles.mp4"  # Define output path
        final_video.write_videofile(output_path, codec="libx264", threads=4)  # Save the final video
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
    video_path = '/Users/mvp/Desktop/videoplayback (1) (1).mp4'
    
    # Test transcription
    print("Starting transcription test...")
    transcription_text = test_extract_audio_and_transcribe(video_path)

    # Test summarization
    if transcription_text:
        print("Transcription received, starting summarization...")
        summary = test_summarize_text(transcription_text)
    else:
        summary = None

    # Test parsing
    if summary:
        print("Summarization received, starting parsing...")
        parsed_summary, timestamps = test_parse_summary_and_timestamps(summary)
    else:
        parsed_summary, timestamps = None, None

    # Test clip extraction
    if timestamps:
        print("Timestamps received, starting clip extraction...")
        test_extract_relevant_clips(video_path, timestamps)

    # Test subtitle addition
    if parsed_summary:
        print("Parsed summary received, starting subtitle addition...")
        test_add_subtitles_to_video(video_path, parsed_summary)

    # Test full summary generation
    print("Testing full video summarization pipeline...")
    test_generate_summary(video_path)

