# Resume & Interview Assistant Bot

## Overview
This project is a web-based application designed to assist job seekers by analyzing uploaded resumes and generating tailored interview questions. It leverages Python, Flask, Streamlit, and advanced libraries like pdfplumber, langchain, sentence-transformers, FAISS, and OpenRouter API to extract resume content, generate embeddings, perform similarity searches, and create interview preparation materials.

## Features
Upload a PDF resume and paste a job description to analyze strengths and gaps.
Uses FAISS for efficient similarity search between resume chunks and job requirements.
Generates personalized interview questions using the OpenRouter API.
Provides a user-friendly interface via Streamlit.

## Required Libraries
```bash
Python 3.8+
Required libraries (install via requirements.txt):
flask
streamlit
requests
python-dotenv
pdfplumber
langchain
sentence-transformers
faiss-cpu
openai
numpy
```


## Installation

### Clone the repository:
```bash
git clone https://github.com/AunMuhammad1211/ResumeInterviewBot
```
```bash
cd RESUMEINTERVIEWBOT
```


### Create a virtual environment and activate it:
To create a virtual environment
```bash
python -m venv venv
```
### To activate the virtual environment
On mac:
```bash
venv/bin/activate
```
On Windows
```bash
venv\Scripts\activate
```


### Install dependencies:
```bash
pip install -r requirements.txt
```


### Set up environment variables:
Create a .env file in the root directory.
Add your OpenRouter API 
key:
```bash
OPENROUTER_API_KEY=your-api-key-here
```

Add .env to .gitignore to keep it secure.



## Running the Application

Start the Flask backend:
```bash 
export FLASK_APP=app/backend/routes.py
flask run
```



### Usage

Upload a PDF resume via the Streamlit interface.
Paste a job description in the provided text area.
Click "Analyze" to view strengths, gaps, and interview questions.



## Deployment
We can deploy this resume interview assistent bot on python anywhere that is a free cloud base platform to deploy your apps. 




