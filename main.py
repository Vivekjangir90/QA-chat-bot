import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()  # take environment variables from .env.
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


vivek_prompt = "vivek_prompt.txt"
gemini_prompt = "gemini_prompt.txt"


def default_prompt(filename):
  try:
    with open(filename, 'r') as file:  
      content = file.read()
    # print(content)  
    return content
  except FileNotFoundError:
    print(f"Error: File '{filename}' not found.")
    return None 
vivek_prompt=default_prompt(vivek_prompt)


history=[{'parts': [{'text': "Greetings! you are  Vivek Jangir, your AI chatbot designed\
                    to assist you with queries related to my skills, projects, and more."}], 'role': 'user'},
        {'parts': [{'text': 'ok.'}], 'role': 'model'},
        {'parts': [{'text': "Don't give your information like i am gemini , a multi-modal ai model, beause you are vivek jangir ai chat bot."}], 'role': 'user'}, 
        {'parts': [{'text': 'ok.'}], 'role': 'model'},
        {'parts': [{'text': f"\n\n{vivek_prompt}"}], 'role': 'user'}, 
        {'parts': [{'text': 'ok.'}], 'role': 'model'}]


def get_gemini_response(question,history):
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=history)
    try:
        response =chat.send_message(question,stream=True)
    except:
        return
    # response =chat.send_message(question,stream=True)
    # response = response.text
    return response

##initialize our streamlit app
st.set_page_config(page_title="Q&A ChatBot main")
st.header("AI Chat Bot")
input=st.text_input("Input: ",key="input")
# agree = st.checkbox('I agree')

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

def history_list():
    try:
        for role,text in st.session_state['chat_history']:
            if role == "you":
                history.append({'parts': [{'text': f"\n\n {text}"}], 'role': 'user'})
            elif role == "Bot":
                history.append({'parts': [{'text': f"{text}"}], 'role': 'model'})
    except:
        pass

submit=st.button("Ask the question")

## If ask button is clicked
if submit or input:
    history_list()
    response=get_gemini_response(input,history)
    # st.write(response)
    st.subheader("The Response is")
    # print(type(response))
    try:
        for text in response:        
            pass
        st.write(response.text)
    except:
        st.write("Please ask me formal questions only.")
        st.write("You need a new conversation.")
        st.write("Please refresh the page. \n Thank You")
        
        
    try:   
        st.session_state['chat_history'].append(("you",input))
        st.session_state['chat_history'].append(("Bot",response.text))
        st.title("History")
        # st.write(st.session_state['chat_history'])
        for role,text in st.session_state['chat_history']:
            print(st.write(role,": \t\t",text))
    except:
        pass    
    # st.title("chat-History")
    # st.write(history)