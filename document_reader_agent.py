# document_reader_agent.py
# Extracts and summarizes content from PDF, DOCX, or text files using skill-aware style

import os
import json
from pathlib import Path
import PyPDF2
import docx

from research_agent_stub import apply_skill_level_tone, extract_glossary_terms

MEMORY_FILE = Path("research_memory.json")

# Load or initialize memory
if MEMORY_FILE.exists():
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        memory = json.load(f)
else:
    memory = {}

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def extract_text_from_txt(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading TXT file: {e}")
        return ""

def extract_text_from_docx(file_path):
    try:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error reading DOCX file: {e}")
        return ""

def summarize_document(text: str, topic: str, level: str):
    short_text = text[:1000]  # Limit to first 1000 characters for prototype
    summary = apply_skill_level_tone(short_text, level)
    glossary = extract_glossary_terms(short_text) if level == "novice" else []

    output = {
        "topic": topic,
        "level": level,
        "summary": summary,
        "glossary_terms": glossary,
        "note": f"Generated from file. Tailored for {level}-level learners."
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
    file_path = input("Enter the path to your .pdf, .docx, or .txt file: ").strip()
    topic_name = input("Enter a topic name for this document: ").strip()
    user_level = input("Enter your skill level (novice/intermediate/advanced): ").strip().lower()

    if file_path.endswith(".pdf"):
        full_text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".txt"):
        full_text = extract_text_from_txt(file_path)
    elif file_path.endswith(".docx"):
        full_text = extract_text_from_docx(file_path)
    else:
        print("Unsupported file type. Only .pdf, .docx, and .txt are supported.")
        exit()

    if not full_text:
        print("No text could be extracted from the file.")
        exit()

    result = summarize_document(full_text, topic_name, user_level)
    print("\n--- Document Reader Agent Output ---")
    print_output(result)
