import json
from datetime import datetime
from pathlib import Path
from research_agent_stub import generate_digestible_output
from web_search_agent import web_search_summary
from evaluator_agent import evaluate_summary
from distribution_agent import distribute_summary

TOPICS_FILE = Path("autonomous_topics.json")
LOG_FILE = Path("autonomous_log.json")

# Load or create topic list
def load_topics():
    if not TOPICS_FILE.exists():
        print("[🚧] No topic file found. Let's create one.")
        topics = []
        while True:
            t = input("Enter a topic (or press Enter to finish): ").strip()
            if not t:
                break
            topics.append(t)
        with open(TOPICS_FILE, "w") as f:
            json.dump({"topics": topics}, f, indent=2)
    else:
        with open(TOPICS_FILE, "r") as f:
            topics = json.load(f).get("topics", [])
    return topics

# Load or create the autonomous log
def load_log():
    if LOG_FILE.exists():
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return []

def save_log(log):
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)

def autonomous_run():
    topics = load_topics()
    log = load_log()
    print(f"\n[🤖] Starting autonomous agent... ({len(topics)} topics)\n")

    for topic in topics:
        print(f"\n🔍 Topic: {topic}")
        level = "novice"  # Default for now; can be expanded to read user profiles

        # Step 1: Try Wikipedia first
        summary_data = generate_digestible_output(topic, level)

        if not summary_data.get("summary") or "no summary" in summary_data["summary"].lower():
            print("⚠️ Wikipedia summary not found, using web search fallback.")
            summary_data = web_search_summary(topic, level)

        if not summary_data.get("summary"):
            print("❌ Skipping. No content available for this topic.")
            continue

        # Step 2: Evaluate
        scores = evaluate_summary(topic, summary_data["summary"], level)

        # Step 3: Distribute
        distribute_summary(topic, summary_data["summary"], level)

        # Step 4: Log
        log_entry = {
            "topic": topic,
            "level": level,
            "timestamp": datetime.now().isoformat(),
            "source": summary_data.get("source", "unknown"),
            "clarity_score": scores.get("clarity"),
            "tone_score": scores.get("tone"),
        }
        log.append(log_entry)
        save_log(log)

    print("\n✅ Autonomous agent run complete.\n")

if __name__ == "__main__":
    autonomous_run()
