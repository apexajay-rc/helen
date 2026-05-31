from urllib.parse import quote, quote_plus

import requests

from utils.audio import speak


HEADERS = {"User-Agent": "Helen-Assistive-AI/1.0"}


def _first_related_text(items):
    for item in items:
        if item.get("Text"):
            return item["Text"]
        nested = item.get("Topics", [])
        text = _first_related_text(nested)
        if text:
            return text
    return ""


def _duckduckgo_answer(query):
    url = (
        "https://api.duckduckgo.com/"
        f"?q={quote_plus(query)}&format=json&no_html=1&skip_disambig=1"
    )
    response = requests.get(url, headers=HEADERS, timeout=8)
    response.raise_for_status()
    data = response.json()
    return (
        data.get("AbstractText")
        or data.get("Answer")
        or _first_related_text(data.get("RelatedTopics", []))
    )


def _wikipedia_answer(query):
    search_url = (
        "https://en.wikipedia.org/w/api.php"
        f"?action=query&list=search&srsearch={quote_plus(query)}"
        "&utf8=1&format=json"
    )
    search_response = requests.get(search_url, headers=HEADERS, timeout=8)
    search_response.raise_for_status()
    matches = search_response.json().get("query", {}).get("search", [])
    if not matches:
        return ""

    title = matches[0]["title"]
    summary_url = (
        "https://en.wikipedia.org/api/rest_v1/page/summary/"
        f"{quote(title, safe='')}"
    )
    summary_response = requests.get(summary_url, headers=HEADERS, timeout=8)
    summary_response.raise_for_status()
    return summary_response.json().get("extract", "")


def search_web(query=""):
    query = query.strip()
    if not query:
        query = input("Search query: ").strip()
    if not query:
        speak("Please provide something to search for.")
        return ""

    try:
        snippet = _duckduckgo_answer(query) or _wikipedia_answer(query)
    except requests.RequestException:
        speak("Sorry, I could not reach the search service.")
        return ""
    except ValueError:
        speak("Sorry, the search service returned an unreadable response.")
        return ""

    if not snippet:
        speak("I could not find a useful search result.")
        return ""

    spoken_snippet = snippet[:700].strip()
    speak(spoken_snippet)
    return spoken_snippet
