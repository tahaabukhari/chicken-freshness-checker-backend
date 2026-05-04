"""
schemas.py — Pydantic Schemas for Data Ingestion & Egress
==========================================================
Defines the strict contract for data coming IN from the IoT device
and data going OUT to the Android app / IoT device.
"""

from datetime import datetime
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# INGESTION — Data coming IN from the IoT device
# ---------------------------------------------------------------------------
class IoTPacketIn(BaseModel):
    """
    Strict schema for the JSON payload sent by the IoT device.

    The IoT device sends field names with special characters
    (e.g. "gas-sensor", "time+date"), so we use Pydantic aliases
    to map them to clean Python attribute names.

    Expected JSON body example:
    {
        "device_id": "DEVICE-001",
        "gas-sensor": 45.2,
        "temp": 28.5,
        "humidity": 72.0,
        "time+date": "2026-05-05T01:38:56Z"
    }
    """

    device_id: str = Field(..., description="Unique IoT device identifier")
    gas_sensor: float = Field(..., alias="gas-sensor", description="Methane/Ammonia gas reading")
    temperature: float = Field(..., alias="temp", description="Temperature in °C")
    humidity: float = Field(..., description="Relative humidity (%)")
    timestamp: datetime = Field(..., alias="time+date", description="ISO-8601 datetime string")

    model_config = {
        "populate_by_name": True,  # Allow access by both alias and field name
        "json_schema_extra": {
            "examples": [
                {
                    "device_id": "DEVICE-001",
                    "gas-sensor": 45.2,
                    "temp": 28.5,
                    "humidity": 72.0,
                    "time+date": "2026-05-05T01:38:56Z",
                }
            ]
        },
    }


# ---------------------------------------------------------------------------
# EGRESS — Data going OUT to the Android App
# ---------------------------------------------------------------------------
class LiveDataOut(BaseModel):
    """
    Clean JSON response for the Android app showing the latest reading.
    """

    device_id: str
    temperature: float
    humidity: float
    gas_sensor: float
    spoilage_percent: float
    category: str
    timestamp: datetime


# ---------------------------------------------------------------------------
# EGRESS — Status/Command response for the IoT device
# ---------------------------------------------------------------------------
class DeviceStatusOut(BaseModel):
    """
    Response sent back to the IoT device when it polls for status/commands.
    Extend this with fields like firmware_update_url, new_interval, etc.
    """

    device_id: str
    status: str = "OK"
    message: str = "No pending commands."
    polling_interval_seconds: int = 30
