\# Agent Documentation



\## Architecture

\- Simple CLI agent that calls Qwen Code API

\- Reads config from `.env.agent.secret`

\- Takes question as command-line argument

\- Outputs JSON with `answer` and `tool\_calls`



\## LLM Provider

\- Qwen Code API running on VM (10.93.26.90:8000)

\- Model: qwen3-coder-plus



\## Usage

```bash

uv run agent.py "What is REST?"

