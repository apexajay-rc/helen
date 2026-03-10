from transformers import pipeline
from utils.audio import speak

qa = pipeline("question-answering")
chat = pipeline("text-generation", model="gpt2")

def process_nlp(command):
    if "what is" in command or "who is" in command:
        answer = qa(question=command, context="OpenAI is an AI company. Google is a search engine.")
        speak(answer['answer'])
    else:
        response = chat(command, max_length=50)[0]['generated_text']
        speak(response)
