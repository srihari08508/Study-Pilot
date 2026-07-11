"""
main.py
--------
Run with:  uvicorn main:app --reload --port 8000

This is the "seamless backend" — one FastAPI app serving:
  - REST CRUD for topics/schedule/progress (instant, deterministic)
  - WebSocket /api/ws for real-time dashboard updates
  - /api/crew/* endpoints that kick off the CrewAI multi-agent crew
    (Scheduler, Tracker, Recommender, Reviewer) in the background and
    push results over the same WebSocket

The MCP server (mcp_server/server.py) runs as a separate process and
shares the same study_data.json, so it's a peer of this app rather than
embedded in it — that's the standard MCP deployment pattern.
"""

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router
from api.ws import manager
from core.automation import start_automation, stop_automation


def _load_run_full_cycle():
    try:
        from crew_agents.crew import run_full_cycle
        return run_full_cycle
    except Exception as e:
        print(f"[startup] CrewAI unavailable: {e}")
        return None

app = FastAPI(title="StudyPilot Agent API", version="2.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


@app.on_event("startup")
async def _on_startup():
    # This is what makes the system autonomous rather than manually
    # triggered: a background loop starts on its own and periodically
    # checks + re-plans + (if needed) runs the full agent cycle, with
    # zero user interaction. See core/automation.py.
    run_full_cycle_fn = _load_run_full_cycle()
    if run_full_cycle_fn is not None:
        start_automation(broadcast_fn=manager.broadcast, run_full_cycle_fn=run_full_cycle_fn)
    else:
        print("[startup] Crew automation is disabled because CrewAI dependencies are missing.")


@app.on_event("shutdown")
async def _on_shutdown():
    stop_automation()


@app.get("/")
def root():
    return {
        "ok": True,
        "service": "studypilot-python-backend",
        "agents": ["Scheduler", "Tracker/Adapter", "Recommender", "Reviewer"],
        "mcp_server": "run separately via mcp_server/server.py",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
