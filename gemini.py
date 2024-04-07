import google.generativeai as genai

def getResponse(prompt, chat):
    resp = chat.send_message(prompt, stream=True)
    return resp