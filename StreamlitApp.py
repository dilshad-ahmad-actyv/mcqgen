import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging
from src.mcqgenerator.MCQgenerator import generate_evaluate_chain

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.callbacks import get_openai_callback
import streamlit as st


with open('/Users/dilshadahmad/GenAI/mcqgen/Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

# Creating the title for the App

st.title("MCQ Creator application with the langchain")

# Create a form using streamlit

with st.form("User Inputs"):
    #file upload
    uploaded_file = st.file_uploader("Upload a pdf or text file")

    # input fields
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)

    # subject
    subject = st.text_input("Insert Subject", max_chars=20)

    #Quiz tone
    tone = st.text_input("Complexity Level of Questions", max_chars=20, placeholder="Simple")

    # Add button
    button = st.form_submit_button("Create MCQs")

    # Check if the button has clicked and all fields have input

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading..."):
            try:
                text = read_file(uploaded_file)
                # Count tokens and const of API call

                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "response_json": json.dumps(RESPONSE_JSON)
                        }
                    )
