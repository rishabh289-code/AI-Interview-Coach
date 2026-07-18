# 🤖 AI Interview Coach

AI Interview Coach is an AI-powered resume analysis application that helps users evaluate their resume against a job description. It uses Retrieval-Augmented Generation (RAG) with FAISS and Sentence Transformers to retrieve the most relevant information from the uploaded resume before sending it to Google's Gemini model. This helps generate more focused and context-aware responses.

---

## 🌐 Live Demo

👉 **Try the application here:**  
https://ai-interview-coach-hf7rr8jaz3koh9wtulxdnt.streamlit.app/

---

## ✨ Features

- Upload a resume in PDF format
- Compare the resume with a job description
- Calculate ATS score
- Generate a professional resume summary
- Identify missing skills
- Suggest improvements to the resume
- Generate HR interview questions
- Generate technical interview questions
- Ask custom questions about the uploaded resume

---

## 🛠️ Technologies Used

- Python
- Streamlit
- GROQ APi
- Sentence Transformers
- FAISS
- pdfplumber
- python-dotenv

---

## ⚙️ How It Works

1. Upload your resume in PDF format.
2. Paste the job description.
3. The resume text is extracted from the PDF.
4. The text is divided into smaller chunks.
5. Sentence Transformers convert the chunks into embeddings.
6. FAISS retrieves the most relevant chunks based on the user's query.
7. GROQ generates the final response using the retrieved information.

---

## 📂 Project Structure

```text
AI-Interview-Coach/
│
├── app.py
├── utils.py
├── prompts.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Running the Project Locally

Clone the repository:

```bash
git clone https://github.com/rishabh289-code/AI-Interview-Coach.git
```

Go to the project folder:

```bash
cd AI-Interview-Coach
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

## 🔑 Environment Variables

Create a `.env` file in the project folder and add your Gemini API key.

```env
GROQ_API_KEY=YOUR_API_KEY
```

---

## 🚀 Future Improvements

- Download analysis as a PDF report
- Support DOCX resumes
- Compare resumes with multiple job descriptions
- Save previous analysis history
- Enhanced ATS dashboard

---

⭐ If you found this project helpful, consider giving it a star. It would be greatly appreciated!