from bs4 import BeautifulSoup
import requests
from utils.audio import speak

def search_web():
    query = input("Search query: ")
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    snippet = soup.find("div", class_="BNeawe").text
    speak(snippet)
