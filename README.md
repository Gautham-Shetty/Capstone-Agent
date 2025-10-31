# Capstone-Agent

Capstone-Agent is an experimental agent framework implementing memory, evaluation, and LLM integration to support episodic and semantic reasoning for conversational and autonomous agent workflows.

This repository collects the core pieces of a research-grade agent: agent orchestration, memory systems (episodic + semantic), a lightweight LLM client wrapper, evaluation harnesses, and optional guardrails and telemetry helpers.

## Features 

- Core agent logic and typed agent models.
- Episodic memory (local, JSON-backed) and a semantic memory store (Chroma embedding DB).
- Implements Pydantic AI agents with encapsulated the core business logic (see `agents.py` and` agents_pydantic.py`).
- Generates vector embeddings using Google GenAI’s text-embedding-004 model for   semantic understanding and retrieval tasks.
- Evaluation runner for automated scenario testing (`evals_runner.py`).
- Minimal MCP / server scaffolding (`mcp_server.py`) for exposing agent endpoints.
- Observability helpers for OpenTelemetry (`otel_setup.py`).
- Presidio-based guardrail utilities (`presideo_guardrail.py`) for PII detection and redaction.

## Key Files and Purpose

Below is a short map of files in this repository and their roles:

- `main.py` — Example entrypoint / runner for the agent.
- `agents.py` — Core agent orchestration and behavior.
- `agents_pydantic.py` — Pydantic models and typed schemas used by agents.
- `models.py` — Domain models and shared data classes.
- `episodic_memory.py` — Local episodic memory implementation (JSON-backed store).
- `semantic_memory.py` — Semantic memory abstraction using Chroma embeddings (data/chroma/semantic).
- `gemini_client.py` — LLM client wrapper; for emdedding the content for semantic retrival and understanding
- `evals_runner.py` — Harness to run evaluation scenarios and collect metrics.
- `mcp_server.py` — Minimal MCP-compatible server scaffolding for exposing the agent as a service.
- `otel_setup.py` — OpenTelemetry setup (traces/metrics helpers).
- `presideo_guardrail.py` — PII/guardrail utilities (Presidio integration).
- `episodic_memory.py` — episodic memory helpers and storage adapter.
- `semantic_memory.py` — semantic search and embedding utilities (uses `data/chroma/semantic`).
- `episodic_memory.py` and `semantic_memory.py` both persist data under `data/`.

Data:

- `data/memory.json` — local episodic memory dump used by the example.
- `data/chroma/semantic/chroma.sqlite3` — Chroma DB used for semantic vectors.

## Environment & credentials
Below are the steps setup the agent 
- uv sync
-  source .venv/bin/activate
- docker run -d -p 16686:16686 -p 4317:4317 -p 4318:4318 jaegertracing/all-in-one:latest to setup the local OTEL

- export GOOGLE_API_KEY={YOUR GOOGLE API KEY}


## Functionalities

- `ingest(text: str, tag: str = "note")` — Redacts PII, creates or updates a semantic-memory entry via `semantic_memory.update` with the provided `tag` metadata, and prints a status plus the redaction report.
- `ask(question: str)` — Queries the agent's "second brain" (`agents.ask_second_brain`) which combines memory retrieval and LLM reasoning; prints the returned answer.
- `memorise(event: str, text: str)` — Redacts `text` and appends it to episodic memory via `episodic_memory.add_to_memory` under the named `event`; prints a success confirmation.
- `askout(question: str)` — Uses an internet-capable agent (`agents.ask_internet`) to fetch web-sourced evidence or answers and prints the web-derived response.
- `joke()` — Executes the `ask_funny_joke` async agent using `asyncio.run` and prints the returned joke to stdout — this is an MCP-integrated agent.

Notes:
- These commands may write to local state (e.g. `data/memory.json`) and the Chroma store under `data/chroma` or call external APIs; ensure required environment variables (LLM/provider keys) are set before running.
- This section only documents `main.py`'s CLI surface — it does not change any runtime code.
 - Both MCP-integrated agents (for example the `joke()` tool) and the web-search agent used by `askout` retrieve or produce content that is indexed into the semantic vector DB (the Chroma store under `data/chroma`). Those indexed vectors act as contextual memory and are used by the `ask` flow to provide evidence, citations, and richer answers to later questions.


# Run evaluators

You can run the evaluators directly. Using the `uv` runner you can run:

```bash
uv run evals_runner.py








