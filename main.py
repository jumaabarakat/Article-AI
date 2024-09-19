from article_functions import detect_language, extract_pdf_text, generate_article_from_content, save_article_to_docx
from flask import Flask, request, jsonify, send_file
import os



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

if __name__ == '__main__':
    app.run(debug=True)



