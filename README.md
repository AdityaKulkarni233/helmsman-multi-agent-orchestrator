# Helmsman-Multi-Agent-Trip-Planner-With-LangGraph

## A Supervisor-driven multi-agent framework built with LangGraph &amp; MCP for orchestrating complex flight and hotel planning workflows

Describe your trip in plain English. Get flight options, hotel ideas, and a day-by-day itinerary.

![Python](https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-multi--agent-1C3C3C)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Groq](https://img.shields.io/badge/LLM-Groq-F55036)
![License](https://img.shields.io/badge/license-MIT-green)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Example](#example)
- [How the Workflow Works](#how-the-workflow-works)
- [Limitations](#limitations)
- [License](#license)
- [Acknowledgments](#acknowledgments)
## Overview

Planning a trip usually means juggling flight sites, hotel searches, blogs, and spreadsheets. TripMate AI collapses that into one request:

> *"Plan a 7-day trip to Tokyo with a budget of $1200 (2 lakhs)"*

Four specialised agents, coordinated by a LangGraph workflow, handle the rest: flight research, hotel discovery, itinerary planning, and a final polished response.

## Features

- ✈️ **Flight research** via the AviationStack API
- 🏨 **Hotel suggestions** via Tavily web search
- 🧠 **Multi-agent orchestration** with LangGraph
- 📝 **Structured day-by-day itineraries**
- 🌐 **FastAPI backend** with a lightweight web UI (Jinja2 + HTML/CSS/JS)
- 💾 **Conversation state persistence** in PostgreSQL
- ⚡ **Fast inference** with Groq-hosted LLMs

## Architecture

```mermaid
flowchart LR
    U[User request] --> API[FastAPI /api/travel]
    API --> G{{LangGraph workflow}}
    G --> F[✈️ Flight agent<br/>AviationStack]
    F --> H[🏨 Hotel agent<br/>Tavily]
    H --> I[🗺️ Itinerary agent]
    I --> R[📝 Final response agent]
    R --> API
    G <-.state.-> DB[(PostgreSQL)]
    API --> U2[Formatted travel plan]
```

| Agent | Responsibility | Data source |
| --- | --- | --- |
| **Flight agent** | Gathers flight-related information for the route | AviationStack |
| **Hotel agent** | Finds accommodation options matching the request | Tavily |
| **Itinerary agent** | Builds a practical day-by-day plan | LLM (Groq) |
| **Final agent** | Merges everything into one polished response | LLM (Groq) |

## Tech Stack

| Layer | Tools |
| --- | --- |
| Language | Python 3.10+ |
| Backend | FastAPI |
| Frontend | Jinja2, HTML, CSS, JavaScript |
| Orchestration | LangGraph, LangChain |
| LLM | Groq |
| Database | PostgreSQL |
| External APIs | Tavily, AviationStack |

## Project Structure

```text
.
├── app.py              # FastAPI app entry point
├── backend.py          # LangGraph travel workflow
├── requirements.txt    # Python dependencies
├── static/             # Static frontend assets
├── templates/          # HTML templates
└── tools/              # Flight and web search integrations
```

## Getting Started

### Prerequisites

- Python 3.10 or newer
- A running PostgreSQL instance
- API keys for [Groq](https://console.groq.com/), [Tavily](https://tavily.com/), and [AviationStack](https://aviationstack.com/)

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root (or copy `.env.example`):

```env
DATABASE_URL=postgresql://user:password@localhost:5432/travel_db
GROQ_API_KEY=your_groq_api_key
AVIATIONSTACK_API_KEY=your_aviationstack_api_key
TAVILY_API_KEY=your_tavily_api_key
DEFAULT_ORIGIN_IATA=HYD 

Note : HYD represents the place from where you want to plan (eg Delhi-DEL, Hyderabad -HYD,etc)
```

| Variable | Description |
| --- | --- |
| `DATABASE_URL` | PostgreSQL connection string used for conversation state |
| `GROQ_API_KEY` | Groq API key for LLM calls |
| `AVIATIONSTACK_API_KEY` | AviationStack key for flight data |
| `TAVILY_API_KEY` | Tavily key for hotel search |
| `DEFAULT_ORIGIN_IATA` | Default departure airport as an IATA code (e.g. `HYD`, `DEL`,`BOM`) |


### 4. Create the database

```bash
createdb travel_db
```

### 5. Run the app

```bash
python app.py
```

Open **http://127.0.0.1:8000/** in your browser.

## API Reference

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/health` | Health check |
| `POST` | `/api/travel` | Submit a travel request |

**Request**

```bash
curl -X POST http://127.0.0.1:8000/api/travel \
  -H "Content-Type: application/json" \
  -d '{"message": "Plan a 7-day trip to Tokyo with a budget of $1200"}'
```

**Request body**

| Field | Type | Description |
| --- | --- | --- |
| `message` | `string` | Natural-language trip request |

FastAPI also serves interactive docs at **http://127.0.0.1:8000/docs**.

## Example

**Input**

```text
Plan a 7-day trip to Tokyo with a budget of of 2 lakhs (or $2100)
```

**Output (abridged)**

```text
✈️ Flights: <flight options>
🏨 Hotels:  <hotel suggestions within budget>
🗺️ Itinerary
  Day 1 – <plan>
  Day 2 – <plan>
  Day 3 – <plan>
```

## How the Workflow Works

1. The user submits a travel request.
2. The flight agent gathers flight-related information.
3. The hotel agent searches for accommodation suggestions.
4. The itinerary agent creates a practical travel plan.
5. The final agent formats the result into a polished response.

## Limitations

- AviationStack primarily provides flight schedule and status data, so results may not include live fares or booking links.
- Hotel suggestions come from web search and should be verified before booking.
- Budget estimates are LLM-generated and approximate.
- Free API tiers have rate limits.

## License

This project is licensed under the Apache License. 

## Acknowledgments

Built with [LangGraph](https://github.com/langchain-ai/langgraph), [LangChain](https://github.com/langchain-ai/langchain), [FastAPI](https://fastapi.tiangolo.com/), [Groq](https://groq.com/), [Tavily](https://tavily.com/), and [AviationStack](https://aviationstack.com/). Intended as a practical example of combining LangGraph agents with real-world APIs.
