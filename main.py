
from article_functions import detect_language, extract_pdf_text, generate_article_from_content
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/generate-article', methods=['POST'])
def generate_article():
    """API endpoint to generate an article."""
    try:
        topic = request.form.get('topic')
        language = request.form.get('language')
        pdf_file = request.files['document']
        
        # Extract content from the uploaded PDF file
        content = extract_pdf_text(pdf_file)

        # Detect the language of the document (if needed)
        document_language = detect_language(content)

        # Generate the article
        article = generate_article_from_content(content, topic, language)

        return jsonify({
            'topic': topic,
            'document_language': document_language,
            'article': article
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)