# Python Reflection Coding Agent 🤖

hey so this is a coding agent i built using LangChain and LangGraph. basically the idea is that the agent doesn't just write code and call it a day — it actually *runs* the code, sees if it works, and if it doesn't, it tries to fix it and runs it again. thats the "reflection" part lol.

it uses Gemini as the brain and runs all the code inside a Docker container so nothing messes up your actual system.

---

## What it does

- takes a coding task from the user
- writes python code to solve it
- runs the code in a sandboxed Docker container
- if there's an error, it reads the error and tries again (keeps looping until it works)
- can also search the web using Tavily if it needs to look something up
- at the end it gives you both the final code AND an explanation of what it did / what errors it ran into along the way

---

## How it works (roughly)

the main agent is built with `langchain` + `langgraph`. it has two tools:

1. **`web_search`** — uses the Tavily API to search the web when it needs info
2. **`coding_environment`** — runs python or shell code inside a Docker container with memory/cpu limits so it cant go crazy

the agent has a system prompt that tells it to behave like a "reflective" developer — meaning it should not just output code blindly, it should actually verify that the code runs correctly before considering the task done.

responses are structured using pydantic, so you always get back:
- `explanation` — what the agent did, what errors it hit, how it fixed them
- `code` — the final working code

theres also a middleware layer that catches tool errors and handles them gracefully so the agent doesnt just crash if something goes wrong.

---

## Project Structure

```
.
├── main.py          # entry point, sets up and runs the agent
├── tools.py         # web_search and coding_environment tools
├── schema.py        # response format + system prompt
├── models.py        # gemini model setup
├── middlewares.py   # tool error handling middleware
├── Dockerfile       # docker image for running code safely
├── pyproject.toml   # dependencies
└── .env             # (you need to create this yourself, see below)
```

---

## Setup

### Requirements

- Python 3.13+
- Docker (must be installed and running)
- uv (for package management) — or you can use pip if you want

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd python-reflection-coding-agent-main
```

### 2. Create a `.env` file

you need api keys for Gemini and Tavily. create a `.env` file in the root directory:

```
GEMINI_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

you can get:
- Gemini API key from [Google AI Studio](https://aistudio.google.com/)
- Tavily API key from [Tavily](https://tavily.com/)

### 3. Build the Docker image

the agent runs code inside a docker container, so you need to build the image first:

```bash
docker build -t agent-python:3.13 .
```

### 4. Install dependencies

```bash
uv sync
```

or with pip:

```bash
pip install -r requirements.txt
```

### 5. Run it

```bash
python main.py
```

it'll ask you what you want, just type your coding task and it'll get to work.

---

## Example

```
Hi how can I help you today?
-> write me a python function that checks if a number is prime
```

the agent will then write the code, run it in docker, verify it works (or fix it if it doesn't), and give you back the final solution with an explanation.

---

## Tech Stack

| Thing | What its used for |
|---|---|
| LangChain | building the agent |
| LangGraph | agent state management + memory |
| Gemini (gemini-3-flash-preview) | the LLM |
| Tavily | web search |
| Docker | sandboxed code execution |
| Pydantic | structured output |

---

## Known Issues / Limitations

- Docker needs to be running before you start the agent, it wont work otherwise
- the coding environment has a memory limit of 100mb and 0.5 cpu so very heavy scripts might not work
- its single-threaded right now, so one conversation at a time
- the model sometimes over-explains things in the explanation field but thats kinda the point i guess

---

## Notes

i made this as a learning project to understand how reflection loops work in AI agents. the core idea is simple — just run → check → fix → repeat — but it was actually pretty interesting to implement with the docker sandboxing and middleware stuff.

feel free to fork it or use it however you want!
