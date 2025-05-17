# 📄 Smart Document Processing Using BERT and OCR

## 🧠 Objective
A smart document processing system that extracts, analyzes, and summarizes information from various document formats (PDF, DOCX, TXT). It leverages **BERT-based NLP** for language understanding and **OCR tools** for image-based text extraction.

---

## 🛠️ Technologies Used

- **NLP Models**: BERT via [Hugging Face Transformers](https://huggingface.co/transformers/)
- **OCR**: Tesseract OCR via `pytesseract`, with image preprocessing using OpenCV
- **Framework**: Flask (for the web interface)
- **Backend Libraries**: 
  - `PyPDF2`, `pdfplumber` (PDF parsing)
  - `python-docx` (DOCX parsing)
  - `pytesseract`, `opencv-python` (OCR)
  - `torch`, `transformers` (for BERT)
  
---

## 🧩 Modules and Features

### 1. Document Upload and Handling
- Upload support for `.pdf`, `.docx`, and `.txt` files through a clean Flask-based web interface.
- Auto-detection and routing to appropriate extraction modules.

### 2. Text Extraction
- **PDFs**: Uses `pdfplumber` or `PyPDF2`
- **Word Docs**: Uses `python-docx`
- **Text Files**: Direct reading

### 3. Image Text Extraction (OCR)
- Documents containing images are processed using:
  - **OpenCV** for preprocessing (grayscale, thresholding, etc.)
  - **Tesseract OCR** for text extraction from images

### 4. NLP-Based Summarization and Analysis
- BERT-powered pipelines for:
  - Text summarization
  - Named Entity Recognition (NER)
  - Key phrase extraction
  - Semantic relationship detection

### 5. Web Interface
- Flask web interface allows:
  - Document upload
  - Display of cleaned, extracted text
  - View of named entities and relationships
  - Display of summarized output
  - OCR-extracted content

---

## ✅ What This Project Does Not Use

- ❌ Multi-modal models like Flamingo, BLIP, CLIP
- ❌ Joint image-text embeddings or end-to-end multi-modal training

> ⚠️ Instead, this project **separately processes** text and image-based content using BERT and OCR respectively.

---

## 🚀 Future Enhancements

To make this project multi-modal and layout-aware, consider integrating:
- **[BLIP / BLIP-2](https://github.com/salesforce/BLIP)** or **[CLIP](https://github.com/openai/CLIP)** for joint image-text analysis
- **[LLaVA](https://llava-vl.github.io/)** for visual question answering
- **[Donut](https://github.com/clovaai/donut)** or **[Pix2Struct](https://github.com/google-research/pix2struct)** for document layout-aware understanding

---

## 📁 Output Files Description

| File Name                 | Description                                                              |
|--------------------------|--------------------------------------------------------------------------|
| `cleaned_text.txt`       | Raw, cleaned textual content extracted from the document                 |
| `extracted_entities.txt` | Named entities like names, dates, locations, and organizations           |
| `extracted_relationships.txt` | Contextual or semantic relationships between detected entities     |
| `extracted_text.txt`     | Combined extracted text from both text and image content                 |
| `summarized_text.txt`    | Final summarized version of the document using BERT-based summarizer     |
| `extracted_images/`      | Folder containing images extracted from the document (if applicable)     |

---

## 🏁 How to Run Locally

### 🔧 Prerequisites
- Python 3.8+
- Tesseract OCR installed and added to system PATH
- Required Python packages:
  ```bash
  pip install -r requirements.txt

