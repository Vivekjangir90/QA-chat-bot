import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load OpenAI model and get response
def get_gemini_response(question, chat_history):
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=chat_history)
    response = chat.send_message(question, stream=True)
    return response, chat

# Initialize Streamlit app
st.set_page_config(page_title="Q&A ChatBot")
st.header("AI Chat Bot")

input_text = st.text_input("Input: ", key="input")

# Load previous chat history from session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

submit_button = st.button("Ask the question")

# If submit button is clicked or input is provided
if submit_button or input_text:
    # Append user input to chat history
    st.session_state['chat_history'].append({'role': 'user', 'text': f'{input_text}'})

    # Get response from Gemini model
    response, chat = get_gemini_response(input_text, st.session_state['chat_history'])
    for text in response:        
        pass
    # Append response to chat history
    st.session_state['chat_history'].append({'role': 'model', 'text': f'{response.text}'})

    # Display response
    st.write("The Response is:")
    # st.write(response.text)

# Display full chat history
st.subheader("Chat History:")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")

