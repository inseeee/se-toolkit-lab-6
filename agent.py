#!/usr/bin/env python3
"""System Agent with query_api tool for Task 3."""

import os
import sys
import json
import requests
from dotenv import load_dotenv

load_dotenv('.env.agent.secret')
load_dotenv('.env.docker.secret')

LLM_API_KEY = os.getenv('LLM_API_KEY')
LLM_API_BASE = os.getenv('LLM_API_BASE')
LLM_MODEL = os.getenv('LLM_MODEL')
LMS_API_KEY = os.getenv('LMS_API_KEY')
AGENT_API_BASE_URL = os.getenv('AGENT_API_BASE_URL', 'http://localhost:42002')

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def safe_path(user_path):
    full_path = os.path.abspath(os.path.join(PROJECT_ROOT, user_path))
    if not full_path.startswith(PROJECT_ROOT):
        return None
    return full_path

def list_files(path="."):
    full_path = safe_path(path)
    if not full_path:
        return "Error: Invalid path"
    try:
        items = os.listdir(full_path)
        return "\n".join(items)
    except Exception as e:
        return f"Error: {str(e)}"

def read_file(path):
    full_path = safe_path(path)
    if not full_path:
        return "Error: Invalid path"
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error: {str(e)}"

def query_api(method="GET", path="/", body=None):
    url = f"{AGENT_API_BASE_URL}{path}"
    headers = {"Authorization": f"Bearer {LMS_API_KEY}"}
    if body:
        headers["Content-Type"] = "application/json"
    try:
        response = requests.request(method, url, headers=headers, json=body, timeout=10)
        return json.dumps({
            "status_code": response.status_code,
            "body": response.text
        })
    except Exception as e:
        return json.dumps({"status_code": 0, "body": str(e)})

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files and directories at a path",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative path from project root"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative path from project root"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_api",
            "description": "Call the backend API. Use for questions about data (item count, scores, status codes).",
            "parameters": {
                "type": "object",
                "properties": {
                    "method": {"type": "string", "description": "HTTP method (GET, POST, etc.)", "default": "GET"},
                    "path": {"type": "string", "description": "API path (e.g., /items/)"},
                    "body": {"type": "object", "description": "Optional JSON body", "default": None}
                },
                "required": ["path"]
            }
        }
    }
]

def call_llm(messages, tools=None):
    payload = {
        "model": LLM_MODEL,
        "messages": messages,
        "temperature": 0.7
    }
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"
    
    response = requests.post(
        f"{LLM_API_BASE}/chat/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LLM_API_KEY}"
        },
        json=payload,
        timeout=30
    )
    response.raise_for_status()
    return response.json()

def execute_tool(tool_name, args):
    if tool_name == "list_files":
        return list_files(**args)
    elif tool_name == "read_file":
        return read_file(**args)
    elif tool_name == "query_api":
        return query_api(**args)
    return f"Error: Unknown tool {tool_name}"

def agentic_loop(question):
    system_prompt = (
        "You are a system agent. You have tools to:\n"
        "- list_files: explore project files\n"
        "- read_file: read file contents\n"
        "- query_api: call the backend API (use for data questions)\n\n"
        "For questions about the system (framework, ports), use read_file.\n"
        "For data questions (item count, status codes), use query_api.\n"
        "When you have the answer, provide it with source if applicable."
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]
    
    tool_calls_log = []
    
    for _ in range(10):
        response = call_llm(messages, tools=TOOLS)
        choice = response['choices'][0]
        message = choice['message']
        
        if not message.get('tool_calls'):
            answer = message.get('content') or ""
            return {
                "answer": answer,
                "tool_calls": tool_calls_log
            }
        
        for tool_call in message['tool_calls']:
            func = tool_call['function']
            name = func['name']
            args = json.loads(func['arguments'])
            result = execute_tool(name, args)
            tool_calls_log.append({
                "tool": name,
                "args": args,
                "result": result
            })
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call['id'],
                "content": result
            })
    
    return {
        "answer": "Maximum iterations reached",
        "tool_calls": tool_calls_log
    }

def main():
    if len(sys.argv) != 2:
        print(json.dumps({"answer": "Error: Please provide a question", "tool_calls": []}))
        sys.exit(1)
    
    question = sys.argv[1]
    try:
        result = agentic_loop(question)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"answer": f"Error: {str(e)}", "tool_calls": []}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()