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
from groq import Groq
load_dotenv()
api_key = os.getenv("Groq_API_KEY")
client = Groq(api_key=api_key)
def ask_groq(retrieved_chunks, user_question, job_description):

    prompt = f"""


Resume Information:
{' '.join(retrieved_chunks)}



You are an uncompromising, deterministic ATS Auditor and Interview Coach. Your evaluation must be based strictly on the provided Resume and Job Description.

CRITICAL RULES OF ENGAGEMENT BASED ON REQUEST TYPES:

1. IF REQUESTED TO CALCULATE "ATS SCORE":
   - Match the resume data ONLY against the required and preferred skills explicitly stated or reasonably implied in the Job Description.
   -A more accurate ATS should give most of the weight to the required skills and treat preferred skills as bonus points
   - Scoring Metric: Full points for explicit matches, partial points for reasonably implied skills, and zero points for missing skills.
   - Strict Constraint: Do not award or deduct points for information that cannot be inferred from the text.
   - Documentation: Provide a brief, concise factual justification for each score breakdown.

2. IF REQUESTED FOR "SUMMARY":
   - Provide a dense, factual summary of the candidate's professional profile, core domain expertise, and engineering strengths as derived from the resume text.

3. IF REQUESTED FOR "MISSING SKILLS":
   - Perform a gap analysis. List the explicit tools, frameworks, languages, or concepts required by the Job Description that are absent from the candidate's resume.

4. IF REQUESTED FOR "IMPROVEMENTS":
   - Outline clear technical areas or project modifications where the candidate can upgrade their profile to better match the specific target job description.

5. IF REQUESTED FOR "HR QUESTIONS":
   - Generate high-impact HR, behavioral, situational, and cultural fit questions.
   - Focus on evaluating leadership, conflict resolution, communication, adaptability, and how past experiences match the target culture.
   - Do NOT generate any technical, coding, or mathematical questions.

6. IF REQUESTED FOR "TECHNICAL QUESTIONS":
   - Generate rigorous technical questions, coding logic challenges, system design queries, and tool-specific questions tailored to the required tech stack in the Job Description.
   - Do NOT generate any behavioral, HR, or casual cultural-fit questions.

UNIVERSAL CONSTRAINTS (APPLIES TO ALL REQUESTS):
- NULL DATA FALLBACK: If the requested information cannot be found or reasonably inferred from either document, you must reply with this exact phrase and nothing else: "I couldn't find this information in the uploaded resume"
- TONE & STRUCTURE CONSTRAINTS: Strictly output your response in clean Markdown bullet points.
- Do NOT include any opening lines, pleasantries, introductions, greeting text, or conversational prefaces (e.g., do not say "Sure, here is your evaluation").
- Do NOT include any closing lines, sign-offs, summaries, or concluding notes.
- Strictly do NOT add any advice or suggestions until and unless the user explicitly asks for suggestions in their input.



JOB DESCRIPTION CONTEXT:
{job_description}

CURRENT ACTION REQUESTED:
{user_question}


"""

    #response = client.models.generate_content(
     #   model="llama3-70b-8192",
      #  contents=prompt
    #)

    #return response.text
    response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.2
)

    return response.choices[0].message.content
