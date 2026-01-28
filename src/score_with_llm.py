import json

import requests

from config import OLLAMA_MODEL, OLLAMA_URL, RESEARCH_PROFILE, TASK


def score_paper(title: str, abstract: str) -> dict:
    prompt = f"""
You are helping a PhD researcher decide whether to read a paper.

Research profile:
{RESEARCH_PROFILE}

Paper:
Title: {title}
Abstract: {abstract}

{TASK}
"""

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.4
        }
    }

    r = requests.post(OLLAMA_URL, json=payload, timeout=180)
    r.raise_for_status()
    data = r.json()
    text = data.get("response", "").strip()
    obj = json.loads(text)
    score = int(obj.get("relevance_score", 0))
    reasons = obj.get("reasons", [])
    return {
        "relevance_score": score,
        "reasons": [str(x) for x in reasons[:3]],
    }

