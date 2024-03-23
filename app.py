import openai
import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = st.secrets["OPENAI_API_KEY"]
import json


created_style = """
    color: #888888; /* Light gray color */
    font-size: 99px; /* Increased font size */
"""
header_style = """
    text-align: center;
    color: white;
    background-color: #0080FF;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 30px;
"""


@st.cache_data
def generate_response(topic):
    content = '''You are a quiz generator. You will be given a particular topic and you will give in response  Mulitple Choice Questions on that topic. Your response should be in the JSON format (a list of dictionaries with each dictionary with six key-value pairs: the question, option1, option2, option3, option4 and correct_option as follows:
         [
         {
            "question": "Which is the correct answer?",
            "option1": "Option 1",
            "option2": "Option 2",
            "option3": "Option 3",
            "option4": "Option 4",
            "correct_option": "Correct answer"}
         {
            "question": "Which is the correct answer?",
            "option1": "Option 1",
            "option2": "Option 2",
            "option3": "Option 3",
            "option4": "Option 4",
            "correct": "Correct answer"}...
         ]
         '''
    messages = [
        {'role': 'system', 'content': content},
        {'role': 'user', 'content': f'{topic}'}
    ]
    response = openai.chat.completions.create(model='gpt-3.5-turbo-0125', messages=messages)
    return response

def main():
    # Check if response is already stored in session state
    st.set_page_config(page_title="Quiz APP", page_icon="❓")
    st.markdown("<p style='{}'>➡️created by 'Muhammad Zain Attiq'</p>".format(created_style), unsafe_allow_html=True)
    st.markdown(f"<h1 style='{header_style}'>Dynamic Quiz App</h1>", unsafe_allow_html=True)
    if 'response' not in st.session_state:
        st.session_state.response = None

    topic = st.text_input("Enter the topic: ")
    # number = st.slider("Number of MCQs",1,20,2)
    if st.button("Generate"):
        # Generate and store response in session state
        response = generate_response(topic)
        response = response.choices[0].message.content
        st.session_state.response = json.loads(response)

    # If response is available, display the quiz
    if st.session_state.response:
        marks = 0
        for i, question in enumerate(st.session_state.response, start=1):
            result = ""
            options = [question[option] for option in ['option1', 'option2', 'option3', 'option4']]
            st.write(question['question'])
            selected = st.radio("Choose one of them:", ["Select from below:"] + options, key=f'{i}')
            if selected == question['correct_option']:
                marks += 1
                result = "Correct!"
            elif selected == "Select from below:":
                result = "Select an option"
            else:
                result = "Wrong!"
            with st.expander(f"Check Question {i}"):
                if result == "Correct!":
                    st.success(result)
                if result == "Select an option":
                    st.warning("Select an option")
                elif result == "Wrong!":
                    st.error(result)

        with st.expander("Check the results: "):
            st.subheader(f"You have got {marks} marks out of 10.")

if __name__ == "__main__":
    main()  
