from utils.audio import speak

qa = None
chat = None
QA_MODEL = "distilbert/distilbert-base-cased-distilled-squad"
CHAT_MODEL = "openai-community/gpt2"

def load_qa_model():
    global qa
    try:
        if qa is None:
            from transformers import pipeline

            qa = pipeline("question-answering", model=QA_MODEL)
    except Exception:
        speak("Sorry, I could not load the language model.")
        return None
    return qa

def load_chat_model():
    global chat
    try:
        if chat is None:
            from transformers import pipeline

            chat = pipeline("text-generation", model=CHAT_MODEL)
    except Exception:
        speak("Sorry, I could not load the language model.")
        return None
    return chat

def process_nlp(command):
    if not command.strip():
        speak("Please say that again.")
        return ""

    if "what is" in command or "who is" in command:
        model = load_qa_model()
        if model is None:
            return ""
        answer = model(question=command, context="OpenAI is an AI company. Google is a search engine.")
        speak(answer['answer'])
        return answer["answer"]
    else:
        model = load_chat_model()
        if model is None:
            return ""
        response = model(
            command,
            max_new_tokens=40,
            truncation=True,
            pad_token_id=50256,
            return_full_text=False,
        )[0]["generated_text"]
        speak(response)
        return response
