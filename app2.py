from dotenv import load_dotenv 
import streamlit as st 
import os 
import PyPDF2 as pdf
import google.generativeai as genai 

load_dotenv()    #  load all envirment variable 


genai.configure(api_key= os.getenv("GOOGLE_API_KEY"))

## gemini Pro response 


def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(input)

    return response.text 

def pdf_text(uploaded_file): # For extracting the text 
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text



#Prompt template
input_prompt = ''' 
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving their resumes. Assign the percentage Matching based 
on Job description and the missing keywords with high accuracy.
also tell me what should i focus on for similaire job with jd like that 
resume:{text}
description:{jd}

'''

#streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS") 
jd = st.text_area("Paste the job description")
uploaded_file = st.file_uploader("Upload Your Resume",type="pdf",help="Please upload the pdf")

submit = st.button("Check your Resume")
if submit:
    if uploaded_file is not None:
        text = pdf_text(uploaded_file)
        input_prompt = input_prompt.format(text=text, jd=jd)
        responce = get_gemini_response(input_prompt)
        st.subheader("The Response is")
        st.write(responce)






