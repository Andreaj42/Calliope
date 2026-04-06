import json

import requests

from config import OLLAMA_MODEL, OLLAMA_URL, RESEARCH_PROFILE, TASK
from utils.logger import getLogger


def score_paper(title: str, abstract: str) -> dict:
    logger = getLogger(__name__)
    logger.info("Starting scoring process...")

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
        "options": {"temperature": 0.4},
    }

    logger.info("---------------------------------------------------")
    logger.info(f"Prompt: {prompt}")

    r = requests.post(OLLAMA_URL, json=payload, timeout=180)
    r.raise_for_status()
    data = r.json()

    logger.info("---------------------------------------------------")
    logger.info(f"Data from LLM: {data}")

    text = data.get("response", "").strip()
    logger.info("---------------------------------------------------")
    logger.info(f"Response from LLM: {text}")

    obj = json.loads(text)

    logger.info("---------------------------------------------------")
    logger.info(f"Parse json from LLM: {obj}")

    score = int(obj.get("relevance_score", 0))
    reasons = obj.get("reasons", [])
    return {
        "relevance_score": score,
        "reasons": [str(x) for x in reasons[:3]],
    }
