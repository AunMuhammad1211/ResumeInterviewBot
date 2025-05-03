import streamlit as st
import requests

st.title("Resume & Interview Assistant Bot")

resume_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
job_description = st.text_area("Paste the job description here")

if st.button("Analyze"):
    if resume_file and job_description:
        try:
            # Send request to Flask backend
            response = requests.post(
                "http://localhost:5000/analyze",
                files={"resume": resume_file},
                data={"job_description": job_description}
            )
            result = response.json()

            if response.status_code != 200 or "analysis" not in result:
                st.error(f"Error from backend: {result.get('error', 'Unknown error')}")
            else:
                # Display analysis
                st.subheader("Analysis")
                st.write("**Strengths:**")
                for strength in result["analysis"]["strengths"]:
                    st.write(strength)
                st.write("**Gaps:**")
                for gap in result["analysis"]["gaps"]:
                    st.write(gap)

                # Display interview questions
                st.subheader("Interview Questions")
                for question in result["questions"]:
                    st.write(question)

        except Exception as e:
            st.error(f"Failed to connect to the backend: {str(e)}")
    else:
        st.error("Please upload a resume and enter a job description.")
