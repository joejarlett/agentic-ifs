# agentic-ifs Demo API

Thin REST wrapper around the **agentic-ifs** library for frontend integration
and interactive exploration. All state is held in-memory -- sessions are lost
on server restart.

**Not clinical software.** For research, simulation, and philosophical
exploration only.

## Installation

From the project root:

```bash
pip install -e ".[demo]"
```

This installs `agentic-ifs` in editable mode along with demo dependencies
(`fastapi`, `uvicorn`).

## Running

```bash
uvicorn demo.app:app --reload --port 8000
```

Interactive Swagger docs are available at **http://localhost:8000/docs**.

## Quick start (curl)

### 1. Create a session

```bash
curl -s -X POST http://localhost:8000/api/v1/sessions \
  -H "Content-Type: application/json" \
  -d '{"initial_self_energy": 0.3}'
```

Returns a `SessionSummary` with a `session_id`. Use that UUID in subsequent
requests.

### 2. Add a Part

```bash
curl -s -X POST http://localhost:8000/api/v1/sessions/{SESSION_ID}/parts \
  -H "Content-Type: application/json" \
  -d '{
    "part_type": "manager",
    "narrative": "The Perfectionist",
    "age": 12,
    "intent": "Keep us safe from criticism",
    "triggers": ["criticism", "failure"],
    "strategies": ["over-preparation", "self-criticism"]
  }'
```

### 3. Run the 6 Fs workflow

```bash
# Step 1: Find
curl -s -X POST http://localhost:8000/api/v1/sessions/{SESSION_ID}/workflow/find \
  -H "Content-Type: application/json" \
  -d '{
    "trailhead_type": "cognitive",
    "intensity": 0.7,
    "description": "Thought: I must not make mistakes",
    "associated_part_id": "{PART_ID}"
  }'

# Step 2: Focus
curl -s -X POST http://localhost:8000/api/v1/sessions/{SESSION_ID}/workflow/focus/{PART_ID}

# Step 3: Flesh Out
curl -s -X POST http://localhost:8000/api/v1/sessions/{SESSION_ID}/workflow/flesh-out/{PART_ID}

# Step 4: Feel Toward (critical gate)
curl -s -X POST http://localhost:8000/api/v1/sessions/{SESSION_ID}/workflow/feel-toward/{PART_ID}

# Step 5: Befriend
curl -s -X POST http://localhost:8000/api/v1/sessions/{SESSION_ID}/workflow/befriend/{PART_ID}

# Step 6: Fear
curl -s -X POST http://localhost:8000/api/v1/sessions/{SESSION_ID}/workflow/fear/{PART_ID}
```

### 4. Export the Parts Map

```bash
curl -s http://localhost:8000/api/v1/sessions/{SESSION_ID}/parts-map
```

Returns a JSON graph compatible with D3.js, Gephi, and Cytoscape.

## CORS configuration

By default, the API allows requests from `http://localhost:5173` and
`http://localhost:3000`. Override with the `CORS_ORIGINS` environment
variable (comma-separated):

```bash
CORS_ORIGINS="http://localhost:5173,http://localhost:3000,https://myapp.example.com" \
  uvicorn demo.app:app --reload --port 8000
```

## API endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/` | Welcome message |
| POST | `/api/v1/sessions` | Create session |
| GET | `/api/v1/sessions` | List session IDs |
| GET | `/api/v1/sessions/{id}` | Get session summary |
| DELETE | `/api/v1/sessions/{id}` | Delete session |
| POST | `/api/v1/sessions/{id}/parts` | Add Part |
| GET | `/api/v1/sessions/{id}/parts` | List Parts |
| GET | `/api/v1/sessions/{id}/parts/{part_id}` | Get Part |
| POST | `/api/v1/sessions/{id}/edges` | Add edge |
| GET | `/api/v1/sessions/{id}/edges` | List edges |
| POST | `/api/v1/sessions/{id}/polarizations` | Add polarization |
| GET | `/api/v1/sessions/{id}/protectors/{exile_id}` | Get protectors |
| POST | `/api/v1/sessions/{id}/workflow/find` | 6Fs Step 1 |
| POST | `/api/v1/sessions/{id}/workflow/focus/{part_id}` | 6Fs Step 2 |
| POST | `/api/v1/sessions/{id}/workflow/flesh-out/{part_id}` | 6Fs Step 3 |
| POST | `/api/v1/sessions/{id}/workflow/feel-toward/{part_id}` | 6Fs Step 4 |
| POST | `/api/v1/sessions/{id}/workflow/befriend/{part_id}` | 6Fs Step 5 |
| POST | `/api/v1/sessions/{id}/workflow/fear/{part_id}` | 6Fs Step 6 |
| POST | `/api/v1/sessions/{id}/blend` | Blend Part |
| POST | `/api/v1/sessions/{id}/unblend/{part_id}` | Unblend Part |
| GET | `/api/v1/sessions/{id}/metrics` | System metrics |
| GET | `/api/v1/sessions/{id}/blends` | Active blends |
| GET | `/api/v1/sessions/{id}/log` | Session log |
| GET | `/api/v1/sessions/{id}/parts-map` | Export Parts Map |

## Note

This demo uses in-memory storage only. All sessions and their state are
lost when the server restarts. This is intentional -- the demo is for
development and exploration, not production use.
