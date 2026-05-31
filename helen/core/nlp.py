from transformers import pipeline
from utils.audio import speak

qa = None
chat = None

def load_models():
    global qa, chat
    try:
        if qa is None:
            qa = pipeline("question-answering")
        if chat is None:
            chat = pipeline("text-generation", model="gpt2")
    except Exception:
        speak("Sorry, I could not load the language model.")
        return False
    return True

def process_nlp(command):
    if not command.strip():
        speak("Please say that again.")
        return ""

    if not load_models():
        return ""
    if "what is" in command or "who is" in command:
        answer = qa(question=command, context="OpenAI is an AI company. Google is a search engine.")
        speak(answer['answer'])
        return answer["answer"]
    else:
        response = chat(command, max_length=50, pad_token_id=50256)[0]['generated_text']
        speak(response)
        return response
