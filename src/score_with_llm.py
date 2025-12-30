import json

import requests

from config import OLLAMA_MODEL, OLLAMA_URL, RESEARCH_PROFILE


def score_paper(title: str, abstract: str) -> dict:
    prompt = f"""
You are helping a PhD researcher decide whether to read a paper.

Research profile:
{RESEARCH_PROFILE}

Paper:
Title: {title}
Abstract: {abstract}

Score rubric (0-100):
- 0-20: unrelated to radio signals or deep learning
- 21-40: mentions DL or wireless but not about signal characteristics (modulation/SNR/bandwidth/frequency)
- 41-60: partly relevant (e.g., RF sensing, spectrum, modulation, or channel-related DL) but not matching the core tasks
- 61-80: clearly relevant to DL for radio signal characterization or closely adjacent tasks
- 81-100: strongly aligned: modulation classification, SNR/bandwidth/center frequency estimation, RF signal parameter inference, dataset/method directly applicable

Important constraints:
- Use the full scale 0-100.
- If unsure, choose a mid value but avoid multiples of 10.

Return ONLY valid JSON with keys:
- relevance_score (integer 0-100)
- reasons (array of up to 3 short strings)
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

