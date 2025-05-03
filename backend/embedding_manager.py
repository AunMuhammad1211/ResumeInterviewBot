import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Load the pre-trained sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_chunk_embeddings(chunk_list):
    """
    Generate embeddings for a list of text chunks from a resume.
    
    Args:
        chunk_list (list): List of Document objects from chunk_data.
    
    Returns:
        numpy.ndarray: Array of embeddings for all chunks.
    """
    embeddings = []
    for data in chunk_list:
        sentences = data.page_content
        encode_sentences = model.encode(sentences, convert_to_numpy=True)
        embeddings.append(encode_sentences)
        print(f"Chunk:\n{sentences[:100]}...\nEmbedding (first 5 values):\n{encode_sentences[:5]}...\n")
    
    embeddings_to_numpy = np.array(embeddings)
    os.makedirs(os.path.dirname('data/'), exist_ok=True)
    np.save('data/resume_embedding.npy', embeddings_to_numpy)
    return embeddings_to_numpy

def generate_job_description_embedding(job_description):
    """
    Generate embedding for a job description.
    
    Args:
        job_description (str): Text of the job description.
    
    Returns:
        numpy.ndarray: Embedding of the job description.
    """
    if not job_description:
        raise ValueError("Job description cannot be empty.")
    encode_description = model.encode(job_description, convert_to_numpy=True)
    os.makedirs(os.path.dirname('data/'), exist_ok=True)
    np.save('data/job_description_embedding.npy', encode_description)
    # print(f"Job Description (first 20 chars):\n{job_description[:20]}...\nEmbedding (first 5 values):\n{encode_description[:5]}...\n")
    return encode_description

def create_faiss_index():
    """
    Create and save a FAISS index for resume embeddings.
    
    Returns:
        faiss.IndexFlatL2: The created FAISS index.
    """
    # Load the embeddings
    resume_emb = np.load('data/resume_embedding.npy')

    # Get dimension (length of embedding vector)
    dim = resume_emb.shape[1]

    # Create FAISS index (L2 distance)
    index = faiss.IndexFlatL2(dim)
    index.add(resume_emb)  # Add resume vectors to the index
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname('data/faiss_index/'), exist_ok=True)
    
    # Save the FAISS index
    faiss.write_index(index, 'data/faiss_index/resume_index.faiss')
    
    return index

def compare_with_faiss(job_embedding, faiss_index_path):
    """
    Compare a job description embedding with resume embeddings using FAISS.
    
    Args:
        job_embedding (numpy.ndarray): Embedding of the job description.
        faiss_index_path (str): Path to the saved FAISS index file.
    
    Returns:
        tuple: (indices, distances) of the top matches.
    """
    # Load the FAISS index
    index = faiss.read_index(faiss_index_path)

    # Search for most similar resume chunk to job description
    k = 5  # Number of top matches you want
    job_embedding = np.array([job_embedding])  # FAISS expects a 2D array
    distances, indices = index.search(job_embedding, k)

    # Flatten indices to 1D array and convert to list
    indices = indices.flatten().tolist()
    distances = distances.flatten().tolist()
    
    return indices, distances


