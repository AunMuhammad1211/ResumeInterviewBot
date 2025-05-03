import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter


def extract_text_from_pdf(pdf_path):
    reader = pdfplumber.open(pdf_path)
    all_text = ""
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            all_text += text + "\n"
            print(f"Page {i + 1}: Text extracted")
        else:
            print(f"Page {i + 1}: No text found")
    reader.close()
    return all_text

def chunk_data(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.create_documents([text])
    return docs
