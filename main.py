from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from research_agent_stub import generate_digestible_output
from content_generator_agent import generate_content
from distribution_agent import distribute_summary
from pathlib import Path
import json
from autonomous_agent import autonomous_run
from pathlib import Path
import os


app = FastAPI()

# Input structure for research/content generation
class AgentInput(BaseModel):
    topic: str
    level: str = "novice"
    format: str = "educational"  # For content generator
    user: str = "default"


# --- ROUTES ---




@app.post("/research")
def run_research(input_data: AgentInput):
    try:
        memory_file = Path(f"research_memory__{input_data.user}.json")
        inbox_file = Path(f"internal_inbox__{input_data.user}.json")

        result = generate_digestible_output(
            input_data.topic,
            input_data.level,
            memory_file=memory_file  # Pass into agent
        )

        distribute_summary(
            input_data.topic,
            result["summary"],
            input_data.level,
            inbox_file=inbox_file
        )

        return {"summary": result["summary"], "user": input_data.user}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate")
def run_content_generation(input_data: AgentInput):
    try:
        content = generate_content(input_data.topic, input_data.format)
        return {"generated_content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/inbox")
def get_inbox():
    inbox_file = Path("internal_inbox.json")
    if inbox_file.exists():
        with open(inbox_file, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {"weekly_digest": {}}

@app.post("/autonomous")
def run_autonomous_pipeline():
    try:
        autonomous_run()
        return {"status": "Autonomous pipeline executed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
def get_system_status():
    status = {}

    # Check autonomous log
    log_file = Path("autonomous_log.json")
    if log_file.exists():
        with open(log_file, "r", encoding="utf-8") as f:
            logs = json.load(f)
            status["last_run"] = logs[-1]["timestamp"] if logs else "Never"
            status["evaluated_topics"] = len(logs)
    else:
        status["last_run"] = "Never"
        status["evaluated_topics"] = 0

    # Check research memory
    memory_file = Path("research_memory.json")
    if memory_file.exists():
        with open(memory_file, "r", encoding="utf-8") as f:
            memory = json.load(f)
            status["memory_entries"] = len(memory)
    else:
        status["memory_entries"] = 0

    # Check inbox
    inbox_file = Path("internal_inbox.json")
    if inbox_file.exists():
        with open(inbox_file, "r", encoding="utf-8") as f:
            inbox = json.load(f)
            digest = inbox.get("weekly_digest", {})
            total = sum(len(v) for k, v in digest.items() if isinstance(v, list))
            status["inbox_items"] = total
    else:
        status["inbox_items"] = 0

    return status
