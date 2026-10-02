# Helmsman-Multi-Agent-Trip-Planner-With-MCP

## A multi-agent travel planner built with LangGraph, where every external data source is exposed as an MCP (Model Context Protocol) server

Describe your trip in plain English. Get flight guidance, hotel ideas, live weather and a day-by-day itinerary.

![Python](https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-multi--agent-1C3C3C)
![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-6E56CF)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Groq](https://img.shields.io/badge/LLM-Groq-F55036)
![License](https://img.shields.io/badge/license-Apache%202.0-blue)

---

## Table of Contents

- [Overview](#overview)
- [What's New in the MCP Version](#whats-new-in-the-mcp-version)
- [Features](#features)
- [Architecture](#architecture)
- [MCP Servers](#mcp-servers)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Example](#example)
- [How the Workflow Works](#how-the-workflow-works)
- [Limitations](#limitations)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

Planning a trip usually means juggling flight sites, hotel searches, weather apps and spreadsheets. This project collapses that into one request:

> *"Plan a 7-day trip to Tokyo with a budget of $1200 (2 lakhs)"*

Five specialised agents, coordinated by a LangGraph workflow, handle the rest: flight research, hotel discovery, weather lookup, itinerary planning, and a final polished response. Each agent gets its data by calling tools on an MCP server instead of using hard-coded API wrappers.

## What's New in the MCP Version

This folder (`Helmsman_with_mcp`) is the MCP rewrite of the original `Helmsman_with_langgraph` app.

| | LangGraph version | MCP version |
| --- | --- | --- |
| Tool access | Direct API wrappers in `tools/` | MCP servers loaded through `langchain-mcp-adapters` |
| Hotel search | Tavily Python client | Tavily remote MCP server |
| Flight data | AviationStack REST calls | AviationStack MCP server |
| Weather | Not included | Custom OpenWeather MCP server |
| Agents | Flight, Hotel, Itinerary, Final | Flight, Hotel, **Weather**, Itinerary, Final |

## Features

- 🔌 **MCP-based tools**: three MCP servers (remote HTTP and local stdio) behind one `MultiServerMCPClient`
- ✈️ **Flight guidance** from AviationStack airport and airline data, summarised by the LLM
- 🏨 **Hotel suggestions** via the Tavily MCP server
- 🌦️ **Current weather and forecast** from a custom OpenWeather MCP server
- 🧠 **Multi-agent orchestration** with LangGraph
- 📝 **Structured day-by-day itineraries** with weather-aware advice
- 🌐 **FastAPI backend** with a lightweight web UI (Jinja2 + HTML/CSS/JS)
- 💾 **Conversation state persistence** in PostgreSQL via the LangGraph checkpointer
- ⚡ **Fast inference** with Groq-hosted LLMs

## Architecture

```mermaid
flowchart LR
    U[User request] --> API[FastAPI /api/travel]
    API --> G{{LangGraph workflow}}
    G --> F[✈️ Flight agent]
    F --> H[🏨 Hotel agent]
    H --> W[🌦️ Weather agent]
    W --> I[🗺️ Itinerary agent]
    I --> R[📝 Final response agent]
    R --> API
    G <-.state.-> DB[(PostgreSQL)]

    F -. MCP .-> AV[AviationStack MCP<br/>stdio via uvx]
    H -. MCP .-> TV[Tavily MCP<br/>streamable HTTP]
    W -. MCP .-> WX[Weather MCP<br/>custom stdio server]
```

| Agent | Responsibility | MCP server |
| --- | --- | --- |
| **Flight agent** | Reads airport and airline data and generates route guidance | AviationStack |
| **Hotel agent** | Finds accommodation options matching the request | Tavily |
| **Weather agent** | Extracts the destination and fetches current weather and forecast | Weather (custom) |
| **Itinerary agent** | Builds a practical, budget-aware day-by-day plan | None (LLM only) |
| **Final agent** | Merges everything into one formatted response | None (LLM only) |

## MCP Servers

All servers are configured in `mcp_client.py` with `MultiServerMCPClient`.

| Server | Transport | How it runs | Tools used |
| --- | --- | --- | --- |
| **Tavily** | `streamable_http` | Hosted at `mcp.tavily.com` | `tavily_search` |
| **AviationStack** | `stdio` | Launched with `uvx aviationstack-mcp` | `list_airports`, `list_airlines` |
| **Weather** | `stdio` | `custom_weather_mcp_server.py`, started with the same Python as the app | `get_current_weather`, `get_forecast` |

Each server is loaded independently, so a failure in one does not prevent the others from working.

## Tech Stack

| Layer | Tools |
| --- | --- |
| Language | Python 3.10+ |
| Backend | FastAPI, Uvicorn |
| Frontend | Jinja2, HTML, CSS, JavaScript |
| Orchestration | LangGraph, LangChain |
| Tool protocol | MCP, `langchain-mcp-adapters` |
| LLM | Groq |
| Database | PostgreSQL (`langgraph-checkpoint-postgres`, `psycopg`) |
| External APIs | Tavily, AviationStack, OpenWeather |

## Project Structure

```text
Helmsman_with_mcp/
├── app.py                        # FastAPI app entry point
├── backend.py                    # LangGraph travel workflow
├── mcp_client.py                 # MCP client config and tool wrappers
├── custom_weather_mcp_server.py  # Custom OpenWeather MCP server
├── mcp_client_test.py            # MCP client checks
├── test_mcp.py                   # MCP connectivity test script
├── test.py                       # Misc test script
├── requirements.txt              # Python dependencies
├── dockerfile                    # Container build
├── static/                       # Frontend assets (CSS, JS)
├── templates/                    # HTML templates
├── tools/                        # Legacy direct-API tools (not used by the MCP flow)
└── excalidraw_files/             # Architecture diagrams
```

## Getting Started

### Prerequisites

- Python 3.10 or newer (the `mcp` package requires it)
- A running PostgreSQL instance
- [`uv`](https://docs.astral.sh/uv/) installed, so `uvx` can launch the AviationStack MCP server
- API keys for [Groq](https://console.groq.com/), [Tavily](https://tavily.com/), [AviationStack](https://aviationstack.com/) and [OpenWeather](https://openweathermap.org/api)

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/helmsman-multi-agent-orchestrator.git
cd helmsman-multi-agent-orchestrator/Helmsman_with_mcp
```

### 2. Create a virtual environment and install dependencies

Keep the virtual environment outside any cloud-synced folder (such as OneDrive) if you can.

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in `Helmsman_with_mcp/`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/travel_db
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
TAVILY_API_KEY=your_tavily_api_key
AVIATIONSTACK_API_KEY=your_aviationstack_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
```

| Variable | Description |
| --- | --- |
| `DATABASE_URL` | PostgreSQL connection string used for conversation state |
| `GROQ_API_KEY` | Groq API key for LLM calls |
| `GROQ_MODEL` | Groq model name; use one your account has access to |
| `TAVILY_API_KEY` | Tavily key, passed to the Tavily MCP server |
| `AVIATIONSTACK_API_KEY` | AviationStack key, passed to the AviationStack MCP server |
| `OPENWEATHER_API_KEY` | OpenWeather key, used by the custom weather MCP server |

Never commit `.env`. It is listed in `.gitignore`.

### 4. Create the database

```bash
createdb travel_db
```

The LangGraph checkpointer creates its own tables on first start.

### 5. Run the app

```bash
python app.py
```

Open **http://127.0.0.1:8000/** in your browser. The first request is slower because the stdio MCP servers start on demand.

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
| `thread_id` | `string` (optional) | Reuse a conversation thread; generated if omitted |

**Response fields**

| Field | Description |
| --- | --- |
| `success` | `true` on success |
| `thread_id` | Conversation thread identifier |
| `answer` | Final formatted travel plan |
| `flight_results` | Flight guidance from the flight agent |
| `hotel_results` | Hotel search results |
| `itinerary` | Draft itinerary |
| `llm_calls` | Number of LLM calls made in the run |

FastAPI also serves interactive docs at **http://127.0.0.1:8000/docs**.

## Example

**Input**

```text
Plan a 7-day trip to Tokyo with a budget of 2 lakhs (or $2100)
```

**Output (abridged)**

```text
🧾 Trip Summary
✈️ Flight Information:  <route, airlines, typical duration, fare range>
🏨 Hotel Suggestions:   <options within budget>
🌦️ Weather:             <current conditions and forecast, packing advice>
🗺️ Day-by-Day Itinerary
  Day 1 – <plan>
  Day 2 – <plan>
💰 Estimated Budget
✅ Final Recommendations
```

## How the Workflow Works

1. The user submits a travel request to `/api/travel`.
2. The **flight agent** calls the AviationStack MCP server for airports and airlines, then the LLM turns that into route guidance.
3. The **hotel agent** calls the Tavily MCP server to search for accommodation.
4. The **weather agent** extracts the destination city with the LLM, then calls the weather MCP server for current conditions and a forecast.
5. The **itinerary agent** combines flights, hotels and weather into a practical plan.
6. The **final agent** formats everything into the response.
7. LangGraph saves the state of each run to PostgreSQL under the thread ID.

## Limitations

- AviationStack provides airport, airline and schedule data, so results do not include live fares or booking links.
- Hotel suggestions come from web search and should be verified before booking.
- Budget estimates are LLM-generated and approximate.
- Free API tiers have rate limits.
- Each request starts the stdio MCP servers, which adds latency.
- Graph nodes are synchronous and call `asyncio.run(...)`, so the `/api/travel` route is a plain `def` and runs in a worker thread.

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `model_not_found` from Groq | Set `GROQ_MODEL` in `.env` to a model your account can use |
| Pylance cannot resolve `mcp` imports | Select the interpreter that has the requirements installed (**Python: Select Interpreter**) |
| `asyncio.run() cannot be called from a running event loop` | Make sure the `/api/travel` route is `def`, not `async def` |
| Connection drops mid-request while developing | Run with `reload=False`, or exclude the venv folder from the reloader |
| AviationStack MCP fails to start | Check that `uv` is installed and `uvx` is on your PATH |

## License

This project is licensed under the Apache License 2.0. See [LICENSE](LICENSE).
