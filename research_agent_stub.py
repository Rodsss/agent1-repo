# research_agent_stub.py
# Research Agent with skill-aware prompting and local memory storage

import requests
import json
import os
from pathlib import Path

MEMORY_FILE = None

# Load or initialize memory
if MEMORY_FILE.exists():
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        memory = json.load(f)
else:
    memory = {}

def get_wikipedia_summary(topic: str) -> str:
    """Fetch a concise summary from Wikipedia for the given topic."""
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ', '_')}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("extract", "No summary found.")
    return "Failed to retrieve summary."

def extract_glossary_terms(summary: str, num_terms: int = 3) -> list:
    """Very basic glossary term extractor using keyword heuristics."""
    import re
    words = re.findall(r'\b[A-Z][a-zA-Z\-]{3,}\b', summary)
    glossary = list(set(words))[:num_terms]
    return glossary

def apply_skill_level_tone(summary: str, level: str) -> str:
    """Adjust summary tone based on skill level."""
    if level == "novice":
        return (
            f"Imagine you're new to the topic. Here's a simple explanation:\n\n"
            f"{summary}\n\n"
            "Try thinking of it like a simplified version of a complex machine."
        )
    elif level == "intermediate":
        return (
            f"Here's a moderately detailed explanation:\n\n"
            f"{summary}\n\n"
            "This version assumes you have some background knowledge."
        )
    elif level == "advanced":
        return (
            f"Technical summary:\n\n"
            f"{summary}\n\n"
            "This version uses domain-specific terminology intentionally."
        )
    else:
        return summary

from pathlib import Path
import json
from datetime import datetime

def generate_digestible_output(topic, level="novice", memory_file=None):
    print(f"[📚] Generating summary for '{topic}' at level: {level}")

    # Set default memory file if none provided
    if memory_file is None:
        memory_file = Path("research_memory.json")

    # Load existing memory (or create new)
    if memory_file.exists():
        with open(memory_file, "r", encoding="utf-8") as f:
            memory = json.load(f)
    else:
        memory = {}

    # Simulate summary (you can hook into real logic here)
    summary = f"This is a skill-aware summary of '{topic}' for a {level} learner."

    glossary = []
    if level == "novice":
        glossary = ["fuel", "injection", "combustion"]  # Example glossary extraction

    # Save to memory
    memory[topic] = {
        "summary": summary,
        "level": level,
        "glossary": glossary,
        "timestamp": datetime.now().isoformat()
    }

    with open(memory_file, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

    return {
        "summary": summary,
        "glossary": glossary,
        "source": "wikipedia"
    }


def print_output(data: dict):
    print(f"\n** Topic: {data['topic']}\nLevel: {data['level']}\n")
    print(f"** Summary:\n{data['summary']}\n")
    if data['glossary_terms']:
        print("** Glossary Terms:")
        for term in data['glossary_terms']:
            print(f"- {term}")
    print(f"\nNote: {data['note']}")

if __name__ == "__main__":
    topic_input = input("Enter a topic to research: ")
    user_level = input("Enter your skill level (novice/intermediate/advanced): ").strip().lower()
    output = generate_digestible_output(topic_input, user_level)
    print("\n--- Research Agent Output ---")
    print_output(output)
