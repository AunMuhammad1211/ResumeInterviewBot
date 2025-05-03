import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter


def extract_text_from_pdf(pdf_path):
    """
    Extract all text from a PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file.
    
    Returns:
        str: Concatenated text from all pages.
    """
    reader = pdfplumber.open(pdf_path)
    all_text = ""
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        # print(text)
        if text:
            all_text += text + "\n"
            print(f"Page {i + 1}: Text extracted")
        else:
            print(f"Page {i + 1}: No text found")
    reader.close()
    return all_text

def chunk_data(text):
    """
    Split text into chunks using RecursiveCharacterTextSplitter.
    
    Args:
        text (str): Full text to be chunked.
    
    Returns:
        list: List of document chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.create_documents([text])
    return docs


# resume_text = extract_text_from_pdf(pdf_path=r'C:\Users\Aun Awan\Desktop\Resume Interview Assistant Bot\data\Profile.pdf')
# data_parts = chunk_data(resume_text)
# Example usage (uncomment to test)
# resume_text = extract_text_from_pdf(pdf_path=r'C:\Users\Aun Awan\Desktop\Resume Interview Assistant Bot\data\Profile.pdf')
# data_chunks = chunk_data(str(resume_text))
# for i, chunk in enumerate(data_chunks):
#     print(f"Chunk {i + 1}: {chunk.page_content}")