import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain


load_dotenv()

key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(openai_api_key = key, model_name = 'gpt-3.5-turbo', temperature=0.3)

TEMPLATE = '''
    Text:{text}
    You are an expert MCQ maker. Given the above text, it's your job to \ create a quiz of {number} multiple choice question for {subject}
    students in {tone} tone. Makes sure the questions are not repeated and Check all the questions to be conforming the text as well.
    Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
    Ensure to make {number} MCQs
    ### RESPONSE_JSON
    {response_json}
'''

TEMPLATE2 = """
    You are an expert english grammarian and writer. Given a multiple choice quiz for {subject} students.\
    You need to evaluate the complexity of the question and give a complete analysis of question of the quiz. 
    Only use max 50 words for complexity. If the quiz is not at per the cognitive and analytical abilities of the students, \
    update the quiz questions which needs to be changed and change the tone such that it perfectly fits the students' ability
    Quiz MCQs:
    {quiz}
    
    Check from an expert English writer of the above quiz:
"""

quiz_generation_prompt = PromptTemplate(
    input_variables=['text', 'number', 'subject', 'tone', 'response_json'],
    template=TEMPLATE
)

quiz_chain = LLMChain(llm = llm, prompts = quiz_generation_prompt, output_key = "quiz", verbose = True)

quiz_evaluation_prompt = PromptTemplate(
    input_variables=['subject', 'quiz'],
    template=TEMPLATE2
)

review_chain = LLMChain(llm = llm,prompts = quiz_evaluation_prompt, output_key = 'review', verbose = True)

generate_evaluate_chain = SequentialChain(
    chains=[quiz_chain, review_chain],
    input_variables=['text', 'number', 'subject', 'tone', 'response_json'],
    output_variables = ['quiz', 'review'],
    verbose=True
    )


