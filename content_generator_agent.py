# content_generator_agent.py
# Uses a research summary to generate educational or marketing content

from pathlib import Path
import json
from random import choice

# Load previous memory from the research agent
MEMORY_FILE = Path("research_memory.json")

if not MEMORY_FILE.exists():
    print("No research memory found. Please run the research agent first.")
    exit()

with open(MEMORY_FILE, "r", encoding="utf-8") as f:
    memory = json.load(f)

def choose_topic():
    topics = list(memory.keys())
    if not topics:
        print("No topics found in memory.")
        exit()
    print("\nAvailable topics:")
    for i, t in enumerate(topics):
        print(f"{i+1}. {t}")
    choice_idx = int(input("\nChoose a topic by number: ")) - 1
    return topics[choice_idx]

def generate_content(topic_data: dict, format_type: str = "educational") -> str:
    topic = topic_data["topic"]
    summary = topic_data["summary"]
    level = topic_data["level"]
    glossary = topic_data["glossary_terms"]

    if format_type == "educational":
        content = (
            f"Here's a beginner-friendly explanation of **{topic}**:\n\n"
            f"{summary}\n\n"
            f"Key terms to remember: {', '.join(glossary)}.\n\n"
            "This is a great starting point for learners who are just getting into the topic."
        )
    elif format_type == "linkedin_post":
        hook = choice([
            f"Ever wondered how {topic} works?",
            f"{topic.capitalize()} is changing the way we think about technology.",
            f"Beginners, here’s a quick dive into {topic}."
        ])
        content = (
            f"{hook}\n\n{summary[:200]}...\n\n"
            "What’s your experience with this concept? Drop a comment below."
        )
    else:
        content = f"Format '{format_type}' not supported yet."

    return content

if __name__ == "__main__":
    topic = choose_topic()
    topic_data = memory[topic]
    format_type = input("Enter content format (educational/linkedin_post): ").strip()
    output = generate_content(topic_data, format_type)

    print("\n--- Generated Content ---\n")
    print(output)
