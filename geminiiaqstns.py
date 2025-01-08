# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 15:25:40 2024

@author: user
"""



from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
import time

# Load environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure the Gemini API client with the API key
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

# Function to generate a single question with retry logic and rate limiting
def generate_question(prompt, retries=3, delay=5):
    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            if "ResourceExhausted" in str(e):
                st.warning(f"Quota limit reached. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                st.error(f"An error occurred: {e}")
                break
    return "Error generating question."

# Function to generate multiple questions of a specific type with rate limiting
def generate_questions(topic, question_type, count):
    questions = []
    batch_size = 10  # Number of questions to generate per batch
    for i in range(0, count, batch_size):
        for _ in range(batch_size):
            prompt = f"Generate a {question_type} on the topic of {topic}. Only provide the question without the answer."
            question = generate_question(prompt)
            questions.append(question)
            # Respect the rate limit by adding a delay
            time.sleep(60 / 15)  # 15 requests per minute limit
    return questions

# Streamlit app configuration
st.set_page_config(page_title="Questions")

st.header("LLM APP")

# When submit is clicked
if st.button("Generate Questions"):
    st.write("Generating questions...")

    mcqs = generate_questions("Intelligent Agents", "multiple-choice question", 100)  # Generate 100 MCQs
    short_answers = generate_questions("Intelligent Agents", "short answer question", 100)  # Generate 100 short answer questions
    long_answers = generate_questions("Intelligent Agents", "long answer question", 100)  # Generate 100 long answer questions

    st.write("## Multiple-Choice Questions")
    for i, question in enumerate(mcqs):
        st.markdown(f"{i + 1}. {question}")

    st.write("## Short Answer Questions")
    for i, question in enumerate(short_answers):
        st.markdown(f"{i + 1}. {question}")

    st.write("## Long Answer Questions")
    for i, question in enumerate(long_answers):
        st.markdown(f"{i + 1}. {question}")