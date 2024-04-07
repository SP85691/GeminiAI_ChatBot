import streamlit as st
import google.generativeai as genai
from gemini import getResponse

intro_text = """
Created By : [Surya Pratap](https://www.github.com/SP85691)\n
This is a chat application powered by Gemini AI 🤖. 
Gemini AI is a generative model developed by Google for conversational purposes. 
You can interact with the AI by typing prompts in the chat interface.
"""

# STREAMLIT SETUP
st.header("💬 Chat with Gemini AI 🤖", anchor=None)
st.divider()
st.sidebar.write("Set your own Gemini API Key [here](https://aistudio.google.com/app/apikey)!")
GEMINI_API_KEY = st.sidebar.text_input("Write Your Prompt", key="chat_input", type="password")
btn = st.sidebar.button("Submit", type="primary")
st.sidebar.divider()
st.sidebar.write(intro_text)
st.sidebar.success("""
This chat application powered by Gemini AI can perform the following tasks:

1. Engage in Conversations: You can interact with Gemini AI by typing prompts in the chat interface. The AI will generate responses based on your prompts.

2. Answer Questions: Ask Gemini AI questions, and it will attempt to provide relevant answers based on its training data.

3. Provide Suggestions: Gemini AI can offer suggestions on various topics, including writing, creativity, and more.

4. Assist with Tasks: Utilize Gemini AI for tasks such as generating text, brainstorming ideas, or providing insights.

Feel free to start a conversation by typing your prompt in the chat input box!
""")
st.sidebar.divider()

# Check if API key is provided
if not GEMINI_API_KEY and not btn:
    st.warning("⚠️ Kindly provide your API key before using this chat app.", icon="🤖")
    st.stop()

# CONFIGURE API
genai.configure(api_key=GEMINI_API_KEY)

# FUNCTION TO GEMINI MODEL
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
        
        # Get Gemini's response
        result = getResponse(prompt, chat)
        response_text = ""
        for chunk in result:
            response_text += chunk.text
        
        # Save Gemini's response to chat history
        st.session_state['chat_history'].append(("Assistant", response_text))
        
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
