# from google.generativeai import GenerativeModel
# from google.generativeai.response import GenerateContentResponse
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st
import os

# from IPython.display import display
# from IPython.display import Markdown



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

bot_history= [
    ({'parts': [{'text': f"\n\n{vivek_prompt}"}], 'role': 'user'}), 
    ({'parts': [{'text': 'Hello! How can i assist you today?'}], 'role': 'model'})
    # {"you": "Me", "text": "{vivek_prompt}"},
    # {"you": "Me", "text": "What are your skills in data science?"},
    # {"bot": ""}  # Initial empty bot response
]
## Function to load OpenAI model and get respones
# raja = [
#   0 : """parts {\n  text: \"\\n\\nWho are you?\"\n}\nrole: \"user\"\n""",
#   1 : """parts {\n  text: \"I am a text based ai model.\"\n}\nrole: \"model\"\n"""
# ]
history=[{'parts': [{'text': '\n\nWho are you'}], 'role': 'user'}, {'parts': [{'text': 'I am a text based ai model.'}], 'role': 'model'}]
# history = [
#     {'role': 'user', 'text': 'hello'},
#     {'role': 'model', 'text': 'Hi there!'},
# ]

def get_gemini_response(question,history):
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=history)
    response =chat.send_message(question,stream=True)
    # response = response.text
    return response, chat

##initialize our streamlit app
st.set_page_config(page_title="Q&A ChatBot main")
st.header("AI Chat Bot")

input=st.text_input("Input: ",key="input")



prompt = """

"""
prompt += input



if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

    # st.session_state.list_history = []


def history_list():
    try:
        for role,text in st.session_state['chat_history']:
            if role == "you":
                history.append({'parts': [{'text': f"\n\n {text}"}], 'role': 'user'})
            else:
                history.append({'parts': [{'text': f"{text}"}], 'role': 'model'})
    except:
        pass
            



submit=st.button("Ask the question")

## If ask button is clicked
if submit or input:
    for role,hist in st.session_state['chat_history']:
        if role == "you":
            bot_history.append(({'parts': [{'text': f"\n\n{hist}"}], 'role': 'user'}))
        else:
            bot_history.append(({'parts': [{'text': f"{hist}"}], 'role': 'model'}))
        
    # messages.append({'role':'model',
    #              'parts':[response.text]})

    # messages.append({'role':'user',
    #              'parts':["Okay, how about a more detailed explanation to a high school student?"]})
    # history_list()
    response,chat=get_gemini_response(prompt,history)
    st.write(response)
    st.subheader("The Response is")
    st.session_state['chat_history'].append(("you",input))
    # print(type(response))
    for text in response:        
        pass
    
    # history.append({'parts': [{'text': f"\n\n {input}"}], 'role': 'user'})
    # history.append({'parts': [{'text': f"{response.text}"}], 'role': 'model'})
    print(st.write(response.text))
    st.session_state['chat_history'].append(("Bot",response.text))
    st.title("History")
    st.write(st.session_state['chat_history'])
    for role,text in st.session_state['chat_history']:
        print(st.write(role,": \t\t",text))
        # if role == "you":
        #     history.append({'parts': [{'text': f"\n\n {text}"}], 'role': 'user'})
        # else:
        #     history.append({'parts': [{'text': f"{text}"}], 'role': 'model'})
   
    st.title("chat-History")
    st.write(history)
    # st.write(type(chat.history))
    # raja = str(chat.history)
    # st.write(raja)
    # st.write(chat.history)
    # st.title("chat")
    # st.write(type(chat))
    # st.write(chat)
        # print(st.write(text.text))
        # print("_"*80)
        # curr_his.append(text.text)
        # bot_curr_response=bot_curr_response+" "+text.text
    # st.session_state.list_history.append({"user":input,"gemini":curr_his})

    # st.write(response)
    # st.write(chat)
    # st.write(bot_history)
    # st.write(chat.history[0])
    # st.write("user :\n\n ", st.session_state.list_history[0]["user"], " \n\n\n\n")
    # st.write("AI :\n\n ", st.session_state.list_history , "\n\n\n")
    # st.write(his[0])
        
        # st.write(f"{role}:{text}")
    # for message in chat.history:
    #     st.write(f'{message.role}: {message.parts[0].text}')