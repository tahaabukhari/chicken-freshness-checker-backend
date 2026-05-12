#!/usr/bin/env python3
import json
import urllib.request
import urllib.error

import os

# Allow overriding the target service URL via SERVICE_URL env var
URL = os.getenv("SERVICE_URL", "https://chicken-freshness-checker-367470746347.us-central1.run.app/api/ingest")

payload = {
    "device_id": "TEST-DEPLOY",
    "gas-sensor": 12.5,
    "temp": 6.2,
    "humidity": 55.1,
    "time+date": "2026-05-13T00:00:00Z",
}

data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(URL, data=data, headers={"Content-Type": "application/json"})

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        print(resp.status)
        print(resp.read().decode())
except urllib.error.HTTPError as e:
    print('HTTPError', e.code)
    try:
        print(e.read().decode())
    except Exception:
        pass
except Exception as e:
    print('Error:', e)
