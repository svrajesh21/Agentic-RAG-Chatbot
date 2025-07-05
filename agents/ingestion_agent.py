import tempfile
import fitz
import pytesseract
from pdf2image import convert_from_bytes
from langchain_community.document_loaders import (
    CSVLoader, Docx2txtLoader, TextLoader, UnstructuredPowerPointLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from utils.mcp import create_mcp_message

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class IngestionAgent:
    def __init__(self):
        self.supported = {
            'pdf': None,
            'docx': Docx2txtLoader,
            'csv': CSVLoader,
            'txt': TextLoader,
            'md': TextLoader,
            'pptx': UnstructuredPowerPointLoader
        }

    def parse_pdf(self, file_storage):
        text = ""
        file_storage.seek(0)
        try:
            doc = fitz.open(stream=file_storage.read(), filetype="pdf")
            for page in doc:
                text += page.get_text()
            if text.strip():
                print("✅ Extracted with PyMuPDF")
                return text
        except Exception as e:
            print("❌ PyMuPDF failed:", e)

        file_storage.seek(0)
        try:
            images = convert_from_bytes(file_storage.read())
            print(f"🔍 OCR fallback triggered - {len(images)} page(s)")
            for i, image in enumerate(images):
                ocr_text = pytesseract.image_to_string(image, config='--psm 6')
                text += ocr_text
        except Exception as e:
            print("❌ OCR failed:", e)

        if not text.strip():
            return "⚠️ OCR failed: No text found in scanned PDF."

        return text

    def ingest(self, file_storage):
        ext = file_storage.filename.split('.')[-1].lower()
        if ext not in self.supported:
            raise ValueError("Unsupported format")

        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
            file_storage.seek(0)
            file_storage.save(tmp.name)

            if ext == 'pdf':
                raw_text = self.parse_pdf(file_storage)
                docs = [Document(page_content=raw_text)]
            else:
                loader = self.supported[ext](tmp.name)
                docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(docs)

        return create_mcp_message("IngestionAgent", "RetrievalAgent", "PARSE_RESULT", {
            "chunks": chunks
        })
