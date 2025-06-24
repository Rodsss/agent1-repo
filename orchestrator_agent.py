# orchestrator_agent.py
# Controls workflow between Research Agent and Content Generator Agent

import subprocess
from pathlib import Path
import json

MEMORY_FILE = Path("research_memory.json")

# --- Helper Functions ---

def run_research_agent():
    print("\n[🧠 Running Research Agent...]")
    subprocess.run(["python", "research_agent_stub.py"])

def run_content_generator():
    print("\n[✍️  Running Content Generator Agent...]")
    subprocess.run(["python", "content_generator_agent.py"])

def run_web_search_agent():
    print("\n[🌐 Running Web Search Agent...]")
    subprocess.run(["python", "web_search_agent.py"])

def run_evaluator_agent():
    print("\n[📊 Running Evaluator Agent...]")
    subprocess.run(["python", "evaluator_agent.py"])

def run_distribution_agent():
    print("\n[📤 Running Distribution Agent...]")
    subprocess.run(["python", "distribution_agent.py"])

def check_memory_exists():
    return MEMORY_FILE.exists() and MEMORY_FILE.stat().st_size > 0

def list_topics():
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        memory = json.load(f)
    return list(memory.keys())

def main():
    print("""
[🔁 Multi-Agent Orchestrator]
Choose a workflow:
1. Run Research Agent only (Wikipedia)
2. Run Content Generator only
3. Full pipeline: Research → Content
4. Run Web Search Agent
5. Run Evaluator Agent
6. Run Distribution Agent
7. View Weekly Digest (Inbox)
8. Exit

    """)

    choice = input("Enter option number: ").strip()

    if choice == "1":
        run_research_agent()
    elif choice == "2":
        if not check_memory_exists():
            print("[⚠️  No research memory found. Please run the Research Agent first.]")
        else:
            run_content_generator()
    elif choice == "3":
        run_research_agent()
        run_content_generator()
    elif choice == "4":
        run_web_search_agent()
    elif choice == "5":
        run_evaluator_agent()
    elif choice == "6":
        run_distribution_agent()
    elif choice == "7":
        print("Exiting orchestrator.")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
