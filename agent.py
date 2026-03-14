#!/usr/bin/env python3
"""Simple LLM caller for Task 1."""

import os
import sys
import json
import requests
from dotenv import load_dotenv

load_dotenv('.env.agent.secret')

LLM_API_KEY = os.getenv('LLM_API_KEY')
LLM_API_BASE = os.getenv('LLM_API_BASE')
LLM_MODEL = os.getenv('LLM_MODEL')

def main():
    if len(sys.argv) != 2:
        print(json.dumps({"answer": "Error: Please provide a question", "tool_calls": []}))
        sys.exit(1)

    question = sys.argv[1]

    try:
        response = requests.post(
            f"{LLM_API_BASE}/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {LLM_API_KEY}"
            },
            json={
                "model": LLM_MODEL,
                "messages": [{"role": "user", "content": question}],
                "temperature": 0.7
            },
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        answer = data['choices'][0]['message']['content']
        print(json.dumps({"answer": answer, "tool_calls": []}))

    except Exception as e:
        print(json.dumps({"answer": f"Error: {str(e)}", "tool_calls": []}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()