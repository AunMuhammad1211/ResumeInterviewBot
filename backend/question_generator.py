import os
from dotenv import load_dotenv
from openai import OpenAI
from .resume_processor import extract_text_from_pdf

# Load environment variables
load_dotenv()

# Initialize OpenRouter client
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),  # Your OpenRouter key
    base_url="https://openrouter.ai/api/v1"   # OpenRouter endpoint
)

def generate_interview_questions(resume_text, num_questions=5):
    prompt = f"Generate {num_questions} relevant interview questions based on this resume:\n\n{resume_text}"

    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",  # Correct OpenRouter model name
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

# Usage
# pdf_path = r'C:\Users\Aun Awan\Desktop\Resume Interview Assistant Bot\data\Profile.pdf'
# resume_text = extract_text_from_pdf(pdf_path)
# if resume_text:
#     questions = generate_interview_questions(resume_text)
#     print(questions)
# else:
#     print("Error: Could not read the PDF.")