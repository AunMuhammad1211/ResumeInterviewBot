import os
from dotenv import load_dotenv
from openai import OpenAI
from .resume_processor import extract_text_from_pdf


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),  
    base_url="https://openrouter.ai/api/v1"  
)

def generate_interview_questions(resume_text, num_questions=10):
    prompt = f"Generate {num_questions} relevant interview questions based on this resume:\n\n{resume_text}"

    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are an HR assistant generating interview questions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )

        questions = response.choices[0].message.content.strip().split("\n")
        return [q for q in questions if q]
    
    except Exception as e:
        print(f"Error: {e}")
        return ["Failed to generate questions. Please check your API key or model name."]
    
def extract_strength_or_gap(text, mode="strength", max_tokens=60):
    try:
        prompt = (
            f"Read the following resume excerpt and extract the key {'strengths' if mode == 'strength' else 'weaknesses or gaps'} "
            "as specific roles, skills, or areas (like 'AI Engineer', 'Communication Skills', 'Data Analyst')."
            f" Be concise and give 1-2 bullet points only:\n\n{text}"
        )
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You extract key strengths or gaps from resume text."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Extraction error ({mode}): {e}")
        return "Unknown"


    

