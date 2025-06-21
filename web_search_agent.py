# web_search_agent.py
# Performs a basic web search and extracts a skill-aware summary from result snippets

import requests
import json
from urllib.parse import quote
from pathlib import Path

from research_agent_stub import apply_skill_level_tone, extract_glossary_terms

MEMORY_FILE = Path("research_memory.json")

# Load or initialize memory
if MEMORY_FILE.exists():
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        memory = json.load(f)
else:
    memory = {}

def duckduckgo_search(query):
    try:
        url = f"https://duckduckgo.com/html/?q={quote(query)}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Very basic extraction from raw HTML
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")
            results = soup.select("a.result__snippet")
            snippets = [res.get_text() for res in results[:5]]
            return "\n".join(snippets)
    except Exception as e:
        print(f"Search failed: {e}")
    return ""

def summarize_web_results(text: str, topic: str, level: str):
    short_text = text[:1000]  # Clip long results
    summary = apply_skill_level_tone(short_text, level)
    glossary = extract_glossary_terms(short_text) if level == "novice" else []

    output = {
        "topic": topic,
        "level": level,
        "summary": summary,
        "glossary_terms": glossary,
        "note": f"Generated from live web search. Tailored for {level}-level learners."
    }

    memory[topic] = output
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

    return output

def print_output(data: dict):
    print(f"\n** Topic: {data['topic']}\nLevel: {data['level']}\n")
    print(f"** Summary:\n{data['summary']}\n")
    if data['glossary_terms']:
        print("** Glossary Terms:")
        for term in data['glossary_terms']:
            print(f"- {term}")
    print(f"\nNote: {data['note']}")

if __name__ == "__main__":
    topic = input("Enter a topic to search the web for: ").strip()
    level = input("Enter your skill level (novice/intermediate/advanced): ").strip().lower()

    print("\n[🔎 Performing web search...]")
    web_data = duckduckgo_search(topic)

    if not web_data:
        print("No results could be retrieved from the web.")
        exit()

    result = summarize_web_results(web_data, topic, level)
    print("\n--- Web Search Agent Output ---")
    print_output(result)
