import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

input_prompt="""
Act like a highly skilled and very experienced ATS(Application Tracking System) for a tech company
with a deep understanding of tech field, data science, data analytics ,software engineering
and machine learning engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving their resumes. Assign the percentage Matching based 
on Job description and the missing keywords with high accuracy
resume:{text}
description:{jd}

Ensure the missing keywords are technical skills, assuming what a hiring manager will be looking in my resume
I want the response in paragraph having the structure :

JD Match :"%"

MissingKeywords : "

Recommendations :""

"""

## streamlit app
st.title("Smart Data Science/Analytics ATS LLM")
st.text("Improve Your Resume ATS score")
jd=st.text_area("Please Paste the Job Description")
uploaded_file=st.file_uploader("Please Upload Your Resume",type="pdf",help="Please upload the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt)
        
        # Dispplay result using st.markdown
        st.markdown(response, unsafe_allow_html=True)