import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Load the pre-trained sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_chunk_embeddings(chunk_list):
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
    if not job_description:
        raise ValueError("Job description cannot be empty.")
    encode_description = model.encode(job_description, convert_to_numpy=True)
    os.makedirs(os.path.dirname('data/'), exist_ok=True)
    np.save('data/job_description_embedding.npy', encode_description)
    print(f"Job Description (first 20 chars):\n{job_description[:20]}...\nEmbedding (first 5 values):\n{encode_description[:5]}...\n")
    return encode_description

def create_faiss_index():
    resume_emb = np.load('data/resume_embedding.npy')
    dim = resume_emb.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(resume_emb)
    
    os.makedirs(os.path.dirname('data/faiss_index/'), exist_ok=True)
    faiss.write_index(index, 'data/faiss_index/resume_index.faiss')
    
    return index

def compare_with_faiss(job_embedding, faiss_index_path):
    index = faiss.read_index(faiss_index_path)

    k = 5  
    job_embedding = np.array([job_embedding]) 
    distances, indices = index.search(job_embedding, k)

    indices = indices.flatten().tolist()
    distances = distances.flatten().tolist()
    
    return indices, distances


