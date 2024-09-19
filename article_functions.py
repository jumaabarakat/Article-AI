import PyPDF2
from langdetect import detect
import openai
from openai import OpenAI

client = OpenAI(
  api_key= ''
)

def extract_pdf_text(pdf_file):
    """Extracts text from the uploaded PDF."""
    print("extract_pdf_text called")
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
        else:
            print(f"Warning: No text extracted from page {reader.pages.index(page)}")
    if not text:
        print("Warning: No text extracted from the PDF")
    return text


def generate_article_from_content(content, topic, language):
    """Generates an article based on the content and topic using OpenAI API."""
    prompt = f"Write an article about {topic} using the following content:\n{content} in {language}"
    
    try:
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant that helps write articles."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000,
            temperature=0.7
        )


        message = completion.choices[0].message.content
        print(message )



        article = message
    except Exception as e:
        print(f"Error generating article: {e}")
        article = "Failed to generate article."
    
    return article

def detect_language(content):
    """Detect the language of the document content."""
    return detect(content)
