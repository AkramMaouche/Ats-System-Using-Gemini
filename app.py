# Steps:
# Filed to put my my JD (Job Description)
# Upload Pdf (Resume)
# Pdf to Image ----> Processing ----> google Gemini Pro 
# Prompt template[multiple prompt]
# this app.py is using Pdf to image meanse our  resume pdf is transformed to an image bytes then analyze it using gemini Falsh model 
# in the other hand app2.py is using Pypdf2 library for transforming it to text for analysing the pdf directly 

from dotenv import load_dotenv 
import streamlit as st 
import os 
from PIL import Image
import pdf2image
import google.generativeai as genai 
import io
import base64


load_dotenv() 


genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))


def get_gemini_responce(input,pdf_content,prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    responce = model.generate_content([input,pdf_content[0],prompt])
    return responce.text 

def input_pdf_setup(uploaded_pdf):
    if uploaded_pdf is not None:
        #Convert Pdf To img
        images=pdf2image.convert_from_bytes(uploaded_file.read(),poppler_path=r'E:\Akram\Genrrative ai\Ats System using Google Gemeni\Release-24.08.0-0\poppler-24.08.0\Library\bin')

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()}
        ]
        
        return pdf_parts 
    else:
        raise FileNotFoundError("No File Uploaded")

    #Streamlit App 

st.set_page_config(page_title="Ats Resume Reviewer")
st.header("ATS Resume Reviewer ���")
input_text = st.text_area("Job Description", key="input") 
uploaded_file = st.file_uploader("Upload Resume file", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully") 


submit1 = st.button("Tell me about the Resume")

submit2 = st.button("How can I improve My Skills")

submit3 = st.button("Percentage match")  

input_prompt1 = """
You are an experienced Human Resource Managerwith teck experience in the field of data science,Big data engeneering,
data analyst, database administrator, your task is to review the provided resume against the job description 
for these profiles. Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
    """

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science,Big data engeneering,
data analyst, database administrator, and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""
if submit1: 
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file) 
        responce = get_gemini_responce(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is:")
        st.write(responce)
    else:
        st.write('Plz import the resume')

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file) 
        responce = get_gemini_responce(input_prompt3,pdf_content,input_text)
        st.subheader("The Response is:")
        st.write(responce)
    else:
        st.write('Plz import the resume')








