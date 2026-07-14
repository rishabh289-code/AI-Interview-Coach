import streamlit as st
from utils import extract_text, chunk_text,createEmbeddings,create_index,search_index,ask_gemini
#st.file_uploader("Choose a file",type=["pdf","docs"])
st.title("AI Interview Coach")
#st.set_page_config(page_title="AI Interview Coach")
upload_file = st.file_uploader("Upload your Resume (PDF)",type=["pdf"])
job_description = st.text_area(
    "Job Description",
    placeholder="Paste the job description from LinkedIn, Naukri, Indeed, or the company's careers page."
)
user_question = st.text_input(
    "Ask a Question",
    placeholder="Example: Calculate ATS score, suggest improvements, or generate interview questions."
)
analyze = st.button("Analyze")

if analyze:
        if upload_file is None:
            st.warning("Please upload your resume")
        elif not user_question:
            st.warning("Please type your question.")
        elif not job_description:
            st.warning("Please give description of your job.")
        else:
            with st.spinner("Please wait... Analyzing your resume..."):
                resume_text = extract_text(upload_file)
                #st.write(resume_text)
                chunks = chunk_text(resume_text)


                #st.write("Number of chunks:", len(chunks))
                embedding = createEmbeddings(chunks)
                #st.write("Embedding shape: ",embedding.shape)

                index=create_index(embedding)
                retrieved_chunks = search_index(
                index,
                user_question,
                chunks
                )
                try:
                    answer=ask_gemini(retrieved_chunks,user_question,job_description)
                    st.subheader("Answer")
                    st.write(answer)
                    st.success("Analysis completed successfully!")
                except Exception:
                     st.error("Unable to generate a response. Please try again.")
      
   
          

          


