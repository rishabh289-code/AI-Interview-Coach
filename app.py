import streamlit as st
from utils import extract_text, chunk_text,createEmbeddings,create_index,search_index,ask_groq
st.title("🤖 AI Interview Coach")
st.caption("Analyze your resume, calculate ATS score, and prepare for interviews using AI.")
st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🤖",
    layout="wide"
)
col1, col2 = st.columns(2)

with col1:
    upload_file = st.file_uploader(
        "📄 Upload Resume (PDF)",
        type=["pdf"]
    )

with col2:
    job_description = st.text_area(
        "📋 Job Description",
        placeholder="Paste the job description here..."
    )
st.subheader("⚡ Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    ats = st.button("📊 ATS Score", use_container_width=True)

with col2:
    summary = st.button("📄 Summary", use_container_width=True)

with col3:
    skills = st.button("📈 Missing Skills", use_container_width=True)

col4, col5, col6 = st.columns(3)

with col4:
    improve = st.button("💡 Improvements", use_container_width=True)

with col5:
    hr = st.button("👨‍💼 HR Questions", use_container_width=True)

with col6:
    tech = st.button("💻 Technical Questions", use_container_width=True)



user_question = st.text_input(
    "💬 Ask Anything",
    placeholder="Example: Compare my resume with this job description."
)

analyze = st.button(
    "🚀 Analyze",
    use_container_width=True
)


if ats:
    user_question = "Calculate the ATS score for my resume by comparing it with the job description. Explain the score and provide suggestions to improve it."

elif summary:
    user_question = "Summarize my resume in a professional manner."

elif skills:
    user_question = "Compare my resume with the job description and list the missing skills."

elif improve:
    user_question = "Suggest improvements to my resume so that it better matches the job description."

elif hr:
    user_question = "Generate 5 HR interview questions based on my resume and the job description."

elif tech:
    user_question = "Generate 5 technical interview questions based on my resume, projects, and the job description."


if analyze or ats or improve or skills or hr or summary or tech:
        if upload_file is None:
            st.warning("Please upload your resume")
        elif not user_question:
            st.warning("Please type your question.")
        elif not job_description:
            st.warning("Please give description of your job.")
        else:
            with st.spinner("🤖 AI is analyzing your resume..."):
                resume_text = extract_text(upload_file)
                chunks = chunk_text(resume_text)

                embedding = createEmbeddings(chunks)

                index=create_index(embedding)
                retrieved_chunks = search_index(
                index,
                user_question,
                chunks
                )
                try:
                    answer=ask_groq(retrieved_chunks,user_question,job_description)
                    
                    st.subheader("📋 Analysis Result")

                    st.success("Analysis completed successfully!")
                    st.write(answer)
                except Exception as e:
                     st.error("Unable to generate a response at the moment")
st.divider()

st.caption(
    "Built using ❤️ Streamlit • FAISS • Sentence Transformers • Groq"
)
      
   
          

          


