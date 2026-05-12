"""
routes.py — API Endpoints
==========================
POST /api/ingest         → IoT device pushes a sensor reading
GET  /api/status/{id}    → IoT device polls for commands
GET  /api/live/{id}      → Android app fetches the latest reading
"""

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import SpoilageReading
from app.schemas import IoTPacketIn, LiveDataOut, DeviceStatusOut
from app.services.analyzer import calculate_spoilage

router = APIRouter(prefix="/api", tags=["IoT"])
logger = logging.getLogger("chicken_freshness_checker.routes")


# ---------------------------------------------------------------------------
# POST  /api/ingest — Receive data from the IoT device
# ---------------------------------------------------------------------------
@router.post("/ingest", response_model=LiveDataOut, status_code=201)
def ingest_reading(
    packet: IoTPacketIn,
    session: Session = Depends(get_session),
):
    """
    Receives a sensor data packet from the IoT device, runs it through
    the spoilage analyzer, persists the result, and returns the processed
    reading.
    """

    logger.info("ingest received from device=%s", packet.device_id)

    # 1. Run the ML / processing pipeline
    spoilage_percent, category = calculate_spoilage(
        temperature=packet.temperature,
        humidity=packet.humidity,
        gas_sensor=packet.gas_sensor,
    )

    # 2. Build the database record
    reading = SpoilageReading(
        device_id=packet.device_id,
        temperature=packet.temperature,
        humidity=packet.humidity,
        gas_sensor=packet.gas_sensor,
        spoilage_percent=round(spoilage_percent, 2),
        category=category,
        timestamp=packet.timestamp,
    )

    # 3. Persist to database
    try:
        session.add(reading)
        session.commit()
        session.refresh(reading)
    except Exception:
        session.rollback()
        logger.exception("Failed to persist reading for device=%s", packet.device_id)
        raise

    logger.info("reading persisted id=%s device=%s", reading.id, reading.device_id)

    # 4. Return the processed reading
    return reading


# ---------------------------------------------------------------------------
# GET  /api/status/{device_id} — IoT device polls for commands
# ---------------------------------------------------------------------------
@router.get("/status/{device_id}", response_model=DeviceStatusOut)
def get_device_status(device_id: str):
    """
    Returns the current status / pending commands for a specific IoT device.

    In production, you would look up a command queue or config table.
    For now this returns a static OK response with a default polling interval.
    """

    return DeviceStatusOut(
        device_id=device_id,
        status="OK",
        message="No pending commands.",
        polling_interval_seconds=30,
    )


# ---------------------------------------------------------------------------
# GET  /api/live/{device_id} — Android app fetches latest reading
# ---------------------------------------------------------------------------
@router.get("/live/{device_id}", response_model=LiveDataOut)
def get_live_data(
    device_id: str,
    session: Session = Depends(get_session),
):
    """
    Returns the most recent spoilage reading for the given device.
    The Android app calls this endpoint to display live sensor data.
    """

    statement = (
        select(SpoilageReading)
        .where(SpoilageReading.device_id == device_id)
        .order_by(SpoilageReading.timestamp.desc())  # type: ignore[union-attr]
        .limit(1)
    )
    reading = session.exec(statement).first()

    if not reading:
        raise HTTPException(
            status_code=404,
            detail=f"No readings found for device '{device_id}'.",
        )

    return reading
