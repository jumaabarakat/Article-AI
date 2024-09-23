from flask import Flask, request, jsonify, send_file
import os
from short_vid import generate_summary, add_subtitles_to_video
from short_video import process_video
# from youtube_generator import extract_video_id, get_video_transcript, generate_summary
# from article_functions import extract_pdf_text, detect_language, generate_article_from_content, save_article_to_docx


app = Flask(__name__)

# @app.route('/generate-article', methods=['POST'])
# def generate_article():
#     """API endpoint to generate an article."""
#     try:
#         # Get topic, language, and uploaded PDF file from the request
#         topic = request.form.get('topic')
#         language = request.form.get('language')
#         pdf_file = request.files['document']

#         # Extract text from the PDF
#         content = extract_pdf_text(pdf_file)

#         # Detect language of the content
#         document_language = detect_language(content)

#         # Generate article based on content, topic, and language
#         article = generate_article_from_content(content, topic, language)

#         # Save the article to a .docx file
#         docx_file_path = save_article_to_docx(article, topic)

#         # Check if the file was successfully created
#         if not os.path.exists(docx_file_path):
#             return jsonify({'error': 'File was not created'}), 500

#         # Return a JSON response confirming the success and file path
#         return jsonify({
#             'topic': topic,
#             'language': language,
#             'document': article
#         }), 200

#     except Exception as e:
#         # Return error message if something goes wrong
#         return jsonify({'error': str(e)}), 400


# @app.route('/generate-summary', methods=['POST'])
# def generate_summary_api():
#     try:
#         data = request.json
#         url = data.get('youtube_url')
#         language = data.get('language', 'English')
#         type_of_summary = data.get('type_of_summary', 'Short')

#         # Validate inputs
#         if not url or language not in ['Arabic', 'English'] or type_of_summary not in ['Detailed', 'Short']:
#             return jsonify({"error": "Invalid input"}), 400
        
#         # Extract video ID from the URL
#         video_id = extract_video_id(url)
#         if not video_id:
#             return jsonify({"error": "Invalid YouTube URL"}), 400
        
#         # Get video transcript
#         transcript_text = get_video_transcript(video_id,language)
        
#         # Generate summary based on the transcript
#         summary = generate_summary(transcript_text, language, type_of_summary)
        
#         # Return the summary as a JSON response
#         return jsonify({
#             "summary": summary,
#             "language": language,
#             "type_of_summary": type_of_summary
#         }), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @app.route('/summarize_video', methods=['POST'])
# def summarize_video_api():
#     try:
#         data = request.json
#         youtube_url = data.get('youtube_url')
#         start_time = data.get('start_time')
#         end_time = data.get('end_time')
#         output_file = "final_summary.mp4"

#         start_time = int(start_time)
#         end_time = int(end_time)

#         # Check for all required fields
#         if not youtube_url or not start_time or not end_time:
#             return jsonify({"error": "Missing required fields. Please provide youtube_url, start_time, and end_time"}), 400

#         processed_video = process_video(youtube_url, start_time, end_time, output_file)

#         if os.path.exists(processed_video):
#             return send_file(processed_video, as_attachment=True)
#         else:
#             return jsonify({"error": "Failed to process the video"}), 500

#     except Exception as e:
#         print(f"Error processing video: {e}")
#         return jsonify({"error": "Internal server error"}), 50

# if __name__ == '__main__':
#     app.run(debug=True)


@app.route('/summarize', methods=['POST'])
def summarize_video():
    """API endpoint to summarize and return the short video."""
    if 'video' not in request.files:
        return {"error": "No video file provided."}, 400

    video = request.files['video']
    video_path = os.path.join(os.getcwd(), video.filename)
    video.save(video_path)

    try:
        # Summarize video and add subtitles
        summarized_text = generate_summary(video_path)
        short_video_path = add_subtitles_to_video(video_path, summarized_text)

        # Return the short video file
        return send_file(short_video_path, as_attachment=True)
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        # Clean up the uploaded video file
        if os.path.exists(video_path):
            os.remove(video_path)

if __name__ == '__main__':
    app.run(debug=True)
