# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 18:48:59 2024

@author: user
"""



import streamlit as st

# Main function
def main():
    st.set_page_config(page_title="Content Generator", page_icon="📝")
    st.header("Content Generator for universities")

    topic = st.text_input("Enter the topic for content generation")
    num_questions = st.number_input("Number of Questions for Each Type", min_value=1, value=5)

    if st.button("Generate"):
        if topic:
            user_input(topic, num_questions)
        else:
            st.warning("Please enter a topic.")

if __name__ == "__main__":
    main()
