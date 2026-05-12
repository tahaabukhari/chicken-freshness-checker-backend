# Feature Test Report

Status: completed

Date: 2026-05-12

Executed tests

- Health-check
	- Command: `curl -s https://chicken-freshness-checker-367470746347.us-central1.run.app/`
	- Result: `{"status":"running","service":"Chicken Freshness Checker API"}` (HTTP 200)

- Ingest endpoint
	- Command: `python scripts/test_post.py`
	- Payload sent:

```json
{
	"device_id": "TEST-DEPLOY",
	"gas-sensor": 12.5,
	"temp": 6.2,
	"humidity": 55.1,
	"time+date": "2026-05-13T00:00:00Z"
}
```

	- Result: HTTP 201
	- Response body:

```json
{"device_id":"TEST-DEPLOY","temperature":6.2,"humidity":55.1,"gas_sensor":12.5,"spoilage_percent":13.28,"category":"fresh","timestamp":"2026-05-13T00:00:00"}
```

Notes
- The earlier 422 JSON error was caused by Windows PowerShell quoting issues when invoking `curl` from the shell. Using a Python client or piping raw JSON avoids that problem.
- `scripts/test_post.py` can be used as an example to POST valid JSON to the service.
