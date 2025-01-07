from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import PyPDF2
import docx
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from transformers import pipeline

# ---------------------------
# ✅ NLTK Configuration
# ---------------------------
nltk.data.path.append('E:/smart_doc_llm/venv/nltk_data')  # Ensure this is correct path for nltk data
try:
    nltk.download('punkt', download_dir='E:/smart_doc_llm/venv/nltk_data')
    nltk.download('stopwords', download_dir='E:/smart_doc_llm/venv/nltk_data')
except Exception as e:
    print(f"[ERROR] NLTK resource download failed: {e}")

# ---------------------------
# ✅ Flask App Initialization
# ---------------------------
app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates'
)
CORS(app)  # Enable CORS for all routes

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize Hugging Face Summarizer
try:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
except Exception as e:
    print(f"[ERROR] HuggingFace pipeline failed to initialize: {e}")
    summarizer = None

# ---------------------------
# ✅ File Extraction Functions
# ---------------------------

def extract_text_from_pdf(pdf_file_path):
    """Extract text from PDF files."""
    try:
        with open(pdf_file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''.join(page.extract_text() or '' for page in reader.pages)
        return text
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {e}")


def extract_text_from_docx(docx_file_path):
    """Extract text from DOCX files."""
    try:
        doc = docx.Document(docx_file_path)
        return "\n".join(para.text for para in doc.paragraphs)
    except Exception as e:
        raise ValueError(f"Error extracting text from DOCX: {e}")


def extract_text_from_txt(txt_file_path):
    """Extract text from TXT files."""
    try:
        with open(txt_file_path, 'r') as file:
            return file.read()
    except Exception as e:
        raise ValueError(f"Error extracting text from TXT: {e}")


# ---------------------------
# ✅ Text Preprocessing
# ---------------------------
def preprocess_text(text):
    """Tokenize, remove punctuation, and filter stopwords."""
    try:
        tokens = word_tokenize(text)
        tokens = [word.lower() for word in tokens if word not in string.punctuation]
        tokens = [word for word in tokens if word not in stopwords.words('english')]
        return " ".join(tokens)
    except Exception as e:
        raise ValueError(f"Error preprocessing text: {e}")


# ---------------------------
# ✅ Text Summarization
# ---------------------------
def summarize_text(text):
    """Summarize the given text."""
    if not summarizer:
        raise ValueError("Summarizer model is not initialized.")
    try:
        summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        raise ValueError(f"Error during text summarization: {e}")


# ---------------------------
# ✅ Routes
# ---------------------------

# 🌐 Serve the Homepage
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


# 🌐 Health Check
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Flask app is up and running'})


# 📂 Serve Static Files Manually (if needed)
@app.route('/public/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)


# 📤 File Upload and Processing
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ['.pdf', '.docx', '.txt']:
        return jsonify({'error': 'Unsupported file format'}), 400

    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Extract text based on file type
        if file_extension == '.pdf':
            text = extract_text_from_pdf(file_path)
        elif file_extension == '.docx':
            text = extract_text_from_docx(file_path)
        elif file_extension == '.txt':
            text = extract_text_from_txt(file_path)
        else:
            return jsonify({'error': 'Unsupported file format'}), 400

        # Preprocess and Summarize
        preprocessed_text = preprocess_text(text)
        summary = summarize_text(preprocessed_text)

        return jsonify({'summary': summary})

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 500
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500


# ---------------------------
# ✅ Run the Flask App
# ---------------------------
if __name__ == '__main__':
    print("[INFO] Starting Flask app...")
    app.run(debug=True, host="127.0.0.1", port=5000)
