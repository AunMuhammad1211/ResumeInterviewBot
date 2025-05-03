from flask import Blueprint, request, jsonify 
from backend.resume_processor import extract_text_from_pdf, chunk_data
from backend.embedding_manager import (
    generate_chunk_embeddings,
    generate_job_description_embedding,
    create_faiss_index,
    compare_with_faiss
)
from backend.question_generator import generate_interview_questions


main = Blueprint('main' ,__name__)


@main.route('/analyze', methods=['POST'])
def analyze():
    try:
        if 'resume' not in request.files or 'job_description' not in request.form:
            return jsonify({"error": "Missing resume file or job description"}), 400

        resume_file = request.files['resume']
        job_description = request.form['job_description']

        resume_text = extract_text_from_pdf(resume_file)
        if not resume_text:
            return jsonify({"error": "No text extracted from the resume"}), 400

        chunks = chunk_data(resume_text)
        if not chunks:
            return jsonify({"error": "No chunks created from the resume text"}), 400

        chunk_embeddings = generate_chunk_embeddings(chunks)
        if chunk_embeddings is None or chunk_embeddings.size == 0:  
            return jsonify({"error": "Failed to generate embeddings for resume chunks"}), 500

        create_faiss_index()

        job_embedding = generate_job_description_embedding(job_description)
        if job_embedding is None or job_embedding.size == 0:  
            return jsonify({"error": "Failed to generate embedding for job description"}), 500

        indices, distances = compare_with_faiss(job_embedding, 'data/faiss_index/resume_index.faiss')

        matched_chunks = [chunks[i] for i in indices if i < len(chunks)]
        strengths = [chunk.page_content if hasattr(chunk, 'page_content') else str(chunk) for chunk in matched_chunks[:3]]
        gaps = [chunk.page_content if hasattr(chunk, 'page_content') else str(chunk)
        for idx, chunk in enumerate(chunks) if idx not in indices[:3]][:3]



        questions = generate_interview_questions(resume_text)
        if not questions:
            return jsonify({"error": "Failed to generate interview questions"}), 500
        questions = [str(q) for q in questions]

        response = {
            "analysis": {
            "strengths": [{"text": chunk.page_content.strip()} for chunk in matched_chunks[:3]],
            "gaps": [{"text": chunk.page_content.strip()} for idx, chunk in enumerate(chunks)
             if idx not in indices[:3]][:3]
             },
            "questions": questions
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
