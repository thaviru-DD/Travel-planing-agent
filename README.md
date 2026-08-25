# Travel Planning Agent

A Python travel assistant that uses LangChain, LangGraph, Ollama, and Tavily to answer travel questions and find places to visit.

## Requirements

- Python 3.9 or newer
- Ollama
- An Ollama model such as `llama3.2`
- A Tavily API key

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Install and start Ollama, then download the model used by the agent:

```bash
ollama pull llama3.2
```

Create a `.env` file in the project root:

```dotenv
TAVILY_API_KEY=your_tavily_api_key
```

Keep `.env` private. It is excluded from Git by `.gitignore`.

## Run the agent

Start the assistant from the project root:

```bash
./.venv/bin/python agent.py
```

Enter a travel question when prompted, for example:

```text
Suggest places to visit in Kandy for a two-day trip.
```

## Test the place tool

```bash
./.venv/bin/python test_place.py
```

## Check dependencies

```bash
./.venv/bin/python -m pip check
```

## Project structure

```text
.
├── agent.py
├── requirements.txt
├── test_place.py
├── test_search.py
└── tools/
	├── calculator.py
	├── distance.py
	├── placessvisit.py
	├── transport.py
	└── weather.py
```
