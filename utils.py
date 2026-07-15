import pdfplumber

def extract_text(uploaded_file):
    text=""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text+"\n"
        
    return text
def chunk_text(text, chunk_size=500, overlap=100):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks

from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
def createEmbeddings(chunks):
    embeddings = model.encode(chunks)
    return embeddings
import faiss
def create_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension);
    index.add(embeddings)
    return index

def search_index(index, user_question, chunks):

    query_embedding = model.encode([user_question])

    distance, indices = index.search(query_embedding, 3)

    retrieved_chunks = []

    for i in indices[0]:
        retrieved_chunks.append(chunks[i])

    return retrieved_chunks
import os
from dotenv import load_dotenv
from google import genai
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
def ask_gemini(retrieved_chunks, user_question, job_description):

    prompt = f"""
You are an experienced HR recruiter.

Use only the resume information provided below.

Resume Information:
{' '.join(retrieved_chunks)}

Job Description:
{job_description}

User Question:
{user_question}

If the user asks for an ATS score, calculate it by comparing the resume with the job description.
Calculate the ATS score by giving higher importance to required skills. Consider preferred skills as bonus points.
If the user asks for multiple things, answer all of them.

Only say "I couldn't find this information in the uploaded resume" if the requested information cannot be found or inferred from the resume or job description.
Do not add any opening or closing line.Strictly answer the question in bullet points
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text
