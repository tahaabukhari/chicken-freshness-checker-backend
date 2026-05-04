"""
models.py — SQLModel Database Tables
=====================================
Defines the persistent data model for IoT spoilage readings.
"""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class SpoilageReading(SQLModel, table=True):
    """
    Represents a single sensor reading from an IoT chicken-spoilage device.

    Fields
    ------
    id              : Auto-incrementing primary key.
    device_id       : Unique identifier string for the IoT device.
    temperature     : Temperature reading in °C from the sensor.
    humidity        : Relative humidity reading (%) from the sensor.
    gas_sensor      : Combined methane/ammonia gas sensor value (float).
    spoilage_percent: Calculated spoilage percentage (0-100).
    category        : Classification label — one of:
                      "fresh", "old-fresh", "semi-spoiled", "spoiled".
    timestamp       : Date+Time when the reading was captured (ISO-8601).
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    device_id: str = Field(index=True)
    temperature: float
    humidity: float
    gas_sensor: float
    spoilage_percent: float
    category: str  # "fresh" | "old-fresh" | "semi-spoiled" | "spoiled"
    timestamp: datetime
