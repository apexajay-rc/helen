from bs4 import BeautifulSoup
import requests
from urllib.parse import quote_plus
from utils.audio import speak

def search_web(query=""):
    query = query.strip()
    if not query:
        query = input("Search query: ").strip()
    if not query:
        speak("Please provide something to search for.")
        return ""

    url = f"https://www.google.com/search?q={quote_plus(query)}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=8)
        res.raise_for_status()
    except requests.RequestException:
        speak("Sorry, I could not reach the search service.")
        return ""

    soup = BeautifulSoup(res.text, "html.parser")
    result = soup.find("div", class_="BNeawe")
    if result is None or not result.get_text(strip=True):
        speak("I could not find a useful search result.")
        return ""

    snippet = result.get_text(" ", strip=True)
    speak(snippet)
    return snippet
