\# Implementation Plan: The System Agent



\*\*Goal:\*\* Add `query\_api` tool to agent from Task 2.



\*\*New tool:\*\*

\- `query\_api(method, path, body)` — calls backend API

\- Authentication: `LMS\_API\_KEY` from `.env.docker.secret`

\- Base URL: from `AGENT\_API\_BASE\_URL` (default http://localhost:42002)



\*\*Agent updates:\*\*

\- Read all config from env vars

\- Update system prompt to choose between wiki tools and query\_api



\*\*Benchmark strategy:\*\*

\- Run `run\_eval.py` and iterate

\- Fix failing questions by improving tool descriptions and system prompt

