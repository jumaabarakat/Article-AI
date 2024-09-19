from flask import Flask, request, jsonify, send_file
import os
from youtube_generator import extract_video_id, get_video_transcript, generate_summary
from article_functions import extract_pdf_text, detect_language, generate_article_from_content, save_article_to_docx


app = Flask(__name__)



@app.route('/generate-article', methods=['POST'])
def generate_article():
    """API endpoint to generate an article."""
    try:
        # Get topic, language, and uploaded PDF file from the request
        topic = request.form.get('topic')
        language = request.form.get('language')
        pdf_file = request.files['document']

        # Extract text from the PDF
        content = extract_pdf_text(pdf_file)

        # Detect language of the content
        document_language = detect_language(content)

        # Generate article based on content, topic, and language
        article = generate_article_from_content(content, topic, language)

        # Save the article to a .docx file
        docx_file_path = save_article_to_docx(article, topic)

        # Check if the file was successfully created
        if not os.path.exists(docx_file_path):
            return jsonify({'error': 'File was not created'}), 500

        # Return a JSON response confirming the success and file path
        return jsonify({
            'topic': topic,
            'language': language,
            'document': article
        }), 200

    except Exception as e:
        # Return error message if something goes wrong
        return jsonify({'error': str(e)}), 400

@app.route('/generate-summary', methods=['POST'])
def generate_summary_api():
    try:
        data = request.json
        url = data.get('youtube_url')
        language = data.get('language', 'English')
        type_of_summary = data.get('type_of_summary', 'Short')

        # Validate inputs
        if not url or language not in ['Arabic', 'English'] or type_of_summary not in ['Detailed', 'Short']:
            return jsonify({"error": "Invalid input"}), 400
        
        # Extract video ID from the URL
        video_id = extract_video_id(url)
        if not video_id:
            return jsonify({"error": "Invalid YouTube URL"}), 400
        
        # Get video transcript
        transcript_text = get_video_transcript(video_id,language)
        
        # Generate summary based on the transcript
        summary = generate_summary(transcript_text, language, type_of_summary)
        
        # Return the summary as a JSON response
        return jsonify({
            "summary": summary,
            "language": language,
            "type_of_summary": type_of_summary
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)



