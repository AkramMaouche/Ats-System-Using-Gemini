# Steps:
# Filed to put my my JD (Job Description)
# Upload Pdf (Resume)
# Pdf to Image ----> Processing ----> google Gemini Pro 
# Prompt template[multiple prompt]

from dotenv import load_dotenv 
import streamlit as st 
import os 
from PL import Image
import pfd2image 
import google.generativeai as genai 
import io
import io
import io

load_dotenv() 


genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))


def get_gemini_responce(input,pdf_content,prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    responce = model.generate_content([input,pdf_content[0],prompt])
    return responce.text 

def input_pdf_setup(uploaded_pdf):
    if uploaded_pdf is not None:
        #Convert Pdf To img
        images = pfd2image.Convert_from_bytes(uploaded_pdf.read())
        first_page = images[0] # entire the whole pdf 
        
        #Convert image to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue() 

        pdf_parts = [
            {
                "mime_type": "image/JPEG",
                "data": base64.b64encode(img_byte_arr).decode()  #encode to base64
            } 
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
    







