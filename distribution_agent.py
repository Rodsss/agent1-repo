# distribution_agent.py
# Routes content from research_memory.json to specific page sections or inbox-style messages

import json
from pathlib import Path
from datetime import datetime

# Section-routing rules based on topic keywords
ROUTING_RULES = {
    "fuel": "mechanical_systems",
    "sensor": "electrical_systems",
    "combustion": "advanced_topics",
    "ignition": "mechanical_systems",
    "beginner": "basic_concepts"
}

MEMORY_FILE = Path("research_memory.json")
INBOX_FILE = Path("internal_inbox.json")
SECTION_STORAGE = Path("section_outputs.json")

# Load memory
if not MEMORY_FILE.exists():
    print("No research memory found. Run another agent first.")
    exit()

with open(MEMORY_FILE, "r", encoding="utf-8") as f:
    memory = json.load(f)

# Load or init inbox and section output
inbox = json.loads(INBOX_FILE.read_text("utf-8")) if INBOX_FILE.exists() else {}
sections = json.loads(SECTION_STORAGE.read_text("utf-8")) if SECTION_STORAGE.exists() else {}

def route_to_section(topic, data):
    """Route summary to a named section based on keyword clusters."""
    topic_lower = topic.lower()
    keywords_to_sections = {
        "mechanical_systems": ["engine", "piston", "combustion", "transmission", "fuel"],
        "electronics": ["electric", "sensor", "voltage", "circuit", "controller"],
        "diagnostics": ["fault", "error", "obd", "diagnose", "malfunction"],
        "learning_guides": ["introduction", "basics", "overview", "fundamentals"],
        "advanced_topics": ["optimization", "efficiency", "dynamics", "calibration"]
    }

    for section, keywords in keywords_to_sections.items():
        if any(kw in topic_lower for kw in keywords):
            target_section = section
            break
    else:
        target_section = "general_knowledge"

    sections.setdefault(target_section, []).append({
        "topic": topic,
        "summary": data["summary"],
        "level": data["level"],
        "timestamp": datetime.now().isoformat()
    })
    print(f"[✅ Routed to section: {target_section}]")

def create_weekly_digest():
    """Compile a summary of topics for inbox-style weekly report."""
    digest = {
        "timestamp": datetime.now().isoformat(),
        "insights": [],
        "recommendations": []
    }
    for topic, data in memory.items():
        digest["insights"].append(f"{topic.title()} ({data['level']}): {data['summary'][:100]}...")
        if data["level"] == "novice":
            digest["recommendations"].append(f"Review glossary terms for '{topic}' to reinforce basics.")

    inbox[digest["timestamp"]] = digest
    print("[📩 Weekly digest sent to inbox]")

def save_outputs():
    with open(INBOX_FILE, "w", encoding="utf-8") as f:
        json.dump(inbox, f, indent=2)
    with open(SECTION_STORAGE, "w", encoding="utf-8") as f:
        json.dump(sections, f, indent=2)

if __name__ == "__main__":
    print("\n[📤 Distribution Agent]")
    for topic, data in memory.items():
        route_to_section(topic, data)

    create_weekly_digest()
    save_outputs()
    print("\n[✅ Distribution complete. Sections and inbox updated.]")
