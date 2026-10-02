"""
Quick smoke test for Helmsman_with_mcp.

Run from the project folder, inside the travelMCP venv:
    python test_mcp.py          # checks each function separately
    python test_mcp.py --full   # also runs the whole LangGraph pipeline
"""
import asyncio
import os
import sys
import time

from dotenv import load_dotenv

load_dotenv()

from mcp_client import (
    run_async,
    extract_destination,
    tavily_mcp_search,
    aviation_mcp_call,
    weather_mcp_search,
    forecast_mcp_search,
)

results = []


def check(name, fn):
    start = time.time()
    try:
        out = fn()
        print(f"[PASS] {name} ({time.time() - start:.1f}s): {str(out)[:120]!r}")
        results.append((name, True))
    except Exception as e:
        print(f"[FAIL] {name}: {type(e).__name__}: {e}")
        results.append((name, False))


# 1. Environment keys (prints only set / MISSING, never the value)
for key in ["GROQ_API_KEY", "TAVILY_API_KEY", "AVIATIONSTACK_API_KEY",
            "OPENWEATHER_API_KEY", "DATABASE_URL"]:
    ok = bool(os.getenv(key))
    print(f"[{'PASS' if ok else 'FAIL'}] env {key}: {'set' if ok else 'MISSING'}")
    results.append((f"env {key}", ok))

# 2. LLM helper (sync)
check("extract_destination (Groq)",
      lambda: extract_destination("3 day trip to Goa from Hyderabad"))

# 3. Each MCP function, through the background loop
check("tavily_mcp_search",
      lambda: run_async(tavily_mcp_search("best hotels in Goa")))
check("aviation list_airports",
      lambda: run_async(aviation_mcp_call("list_airports")))
check("weather_mcp_search",
      lambda: run_async(weather_mcp_search("Goa")))
check("forecast_mcp_search",
      lambda: run_async(forecast_mcp_search("Goa")))


# 4. Calling run_async from inside a running loop (what FastAPI does)
async def inside_running_loop():
    return run_async(weather_mcp_search("Goa"))


check("run_async inside a running event loop",
      lambda: asyncio.run(inside_running_loop()))

# 5. Optional: the full graph with the Postgres checkpointer
if "--full" in sys.argv:
    def full_run():
        from backend import run_travel_agent
        out = run_travel_agent("2 day trip to Goa from Hyderabad")
        return f"llm_calls={out['llm_calls']}, answer={out['answer'][:80]}"

    check("full run_travel_agent", full_run)

print("\n==== SUMMARY ====")
for name, ok in results:
    print(f"{'PASS' if ok else 'FAIL'}  {name}")
sys.exit(0 if all(ok for _, ok in results) else 1)