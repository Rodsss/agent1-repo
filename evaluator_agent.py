# evaluator_agent.py
# Scores research summaries based on clarity, tone, and alignment with skill level

import json
from pathlib import Path
from textblob import TextBlob

MEMORY_FILE = Path("research_memory.json")
EVAL_FILE = Path("evaluation_results.json")

# Load research memory
if not MEMORY_FILE.exists():
    print("No research memory found. Run another agent first.")
    exit()

with open(MEMORY_FILE, "r", encoding="utf-8") as f:
    memory = json.load(f)

def evaluate_clarity(text):
    blob = TextBlob(text)
    score = 100 - abs(len(text) - 700) * 0.05  # Penalize overly short/long responses
    score = min(max(score, 0), 100)
    return round(score, 1)

def evaluate_tone_match(level, text):
    if level == "novice":
        simple_terms = sum(1 for word in text.split() if len(word) <= 5)
        ratio = simple_terms / max(len(text.split()), 1)
        score = ratio * 100
    elif level == "advanced":
        complex_terms = sum(1 for word in text.split() if len(word) > 7)
        ratio = complex_terms / max(len(text.split()), 1)
        score = ratio * 100
    else:
        score = 70  # Neutral estimate
    return round(min(score, 100), 1)

def evaluate_summary(topic_data):
    text = topic_data.get("summary", "")
    level = topic_data.get("level", "unknown")

    return {
        "Clarity Score": evaluate_clarity(text),
        "Tone Fit Score": evaluate_tone_match(level, text),
        "Overall Comment": f"Evaluation complete for skill level: {level}."
    }

def print_evaluation(topic, evaluation):
    print(f"\n🔎 Evaluation for: {topic}")
    for k, v in evaluation.items():
        print(f"{k}: {v}")

def save_evaluation(topic, evaluation):
    if EVAL_FILE.exists():
        with open(EVAL_FILE, "r", encoding="utf-8") as f:
            all_evals = json.load(f)
    else:
        all_evals = {}

    all_evals[topic] = evaluation
    with open(EVAL_FILE, "w", encoding="utf-8") as f:
        json.dump(all_evals, f, indent=2)

def get_top_and_low_scores():
    if not EVAL_FILE.exists():
        return [], []
    with open(EVAL_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    scored = [(k, v["Clarity Score"], v["Tone Fit Score"]) for k, v in data.items()]
    scored.sort(key=lambda x: (x[1] + x[2]) / 2, reverse=True)
    return scored[:3], scored[-3:]

if __name__ == "__main__":
    print("\nTopics available for evaluation:")
    topics = list(memory.keys())
    for i, t in enumerate(topics):
        print(f"{i+1}. {t}")

    idx = int(input("\nSelect topic number to evaluate: ")) - 1
    chosen_topic = topics[idx]
    topic_data = memory[chosen_topic]

    eval_result = evaluate_summary(topic_data)
    print_evaluation(chosen_topic, eval_result)
    save_evaluation(chosen_topic, eval_result)

    print("\n[📊 Evaluation saved to evaluation_results.json]")

    top, low = get_top_and_low_scores()
    print("\n🏅 Top Scoring Topics:")
    for t, c, tone in top:
        print(f"- {t}: Clarity={c}, Tone Fit={tone}")

    print("\n🔻 Lowest Scoring Topics:")
    for t, c, tone in low:
        print(f"- {t}: Clarity={c}, Tone Fit={tone}")
