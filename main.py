from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from research_agent_stub import generate_digestible_output
from content_generator_agent import generate_content
from distribution_agent import distribute_summary
from pathlib import Path
import json
from autonomous_agent import autonomous_run


app = FastAPI()

# Input structure for research/content generation
class AgentInput(BaseModel):
    topic: str
    level: str = "novice"
    format: str = "educational"  # for content generator

# --- ROUTES ---




@app.post("/research")
def run_research(input_data: AgentInput):
    try:
        result = generate_digestible_output(input_data.topic, input_data.level)
        distribute_summary(input_data.topic, result["summary"], input_data.level)
        return {"summary": result["summary"], "routed": True}
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
