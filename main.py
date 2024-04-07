import streamlit as st
import google.generativeai as genai
from gemini import getResponse
import os 
from dotenv import load_dotenv

load_dotenv()

intro_text = """
Created By : [Surya Pratap](https://www.github.com/SP85691)\n
This is a chat application powered by Baymax AI 🤖. 
Baymax AI is a generative model developed by Google for conversational purposes. 
You can interact with the AI by typing prompts in the chat interface.
"""

# STREAMLIT SETUP
st.header("💬 Chat with Baymax AI 🤖", anchor=None)
st.divider()
st.warning("API key will be required after two days.", icon="🤖")
st.sidebar.write("Set your own Baymax API Key [here](https://aistudio.google.com/app/apikey)!")
GEMINI_API_KEY = st.sidebar.text_input("Write Your Prompt", key="chat_input", type="password")
btn = st.sidebar.button("Submit", type="primary")
st.sidebar.divider()
st.sidebar.write(intro_text)
st.sidebar.success("""
This chat application powered by Baymax AI can perform the following tasks:

1. Engage in Conversations: You can interact with Baymax AI by typing prompts in the chat interface. The AI will generate responses based on your prompts.

2. Answer Questions: Ask Baymax AI questions, and it will attempt to provide relevant answers based on its training data.

3. Provide Suggestions: Baymax AI can offer suggestions on various topics, including writing, creativity, and more.

4. Assist with Tasks: Utilize Baymax AI for tasks such as generating text, brainstorming ideas, or providing insights.

Feel free to start a conversation by typing your prompt in the chat input box!
""")
st.sidebar.divider()

# Check if API key is provided
if not GEMINI_API_KEY and not btn:
    # st.warning("⚠️ Kindly provide your API key before using this chat app.", icon="🤖")
    # st.stop()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# CONFIGURE API
genai.configure(api_key=GEMINI_API_KEY)

# FUNCTION TO BAYMAX MODEL
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Initialize chat history in session state if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

def main():
    prompt = st.chat_input("Write Your Prompt")
    if prompt:
        # Save user prompt to chat history
        st.session_state['chat_history'].append(("User", prompt))
        
        # Get Baymax's response
        result = getResponse(prompt, chat)
        response_text = ""
        for chunk in result:
            response_text += chunk.text
        
        # Save Baymax's response to chat history
        st.session_state['chat_history'].append(("Baymax", response_text))
        
    # Display chat history
    for role, Res in st.session_state['chat_history']:
        if role == "User":
            with st.chat_message("user"):
                st.write(Res)
        else:
            message = st.chat_message("assistant")
            message.write(Res)            
        
if __name__ == '__main__':
    main()
