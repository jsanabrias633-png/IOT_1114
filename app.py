import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from dotenv import load_dotenv
from flask import Flask, request, render_template, jsonify

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
logger = logging.getLogger(__name__)


def _safe_int(value: Optional[str], fallback: int) -> int:
    try:
        return int(value) if value is not None else fallback
    except (TypeError, ValueError):
        return fallback


REFRESH_SECONDS = _safe_int(os.getenv("STATUS_REFRESH_SECONDS"), 5)
HOST = os.getenv("FLASK_HOST", "0.0.0.0")
PORT = _safe_int(os.getenv("FLASK_PORT"), 5000)
DEBUG_MODE = os.getenv("FLASK_DEBUG", "true").lower() in {"1", "true", "yes"}

sensor_data = {"temperature": None, "humidity": None}
last_update_at: Optional[datetime] = None
app_started_at = datetime.now(timezone.utc)

CONNECTED_THRESHOLD = timedelta(seconds=10)
STALE_THRESHOLD = timedelta(seconds=30)


def _calculate_status(timestamp: Optional[datetime]) -> str:
    """Return connection status based on how recent the last update was."""
    if timestamp is None:
        return "offline"

    elapsed = datetime.now(timezone.utc) - timestamp
    if elapsed <= CONNECTED_THRESHOLD:
        return "connected"
    if elapsed <= STALE_THRESHOLD:
        return "stale"
    return "offline"


@app.route("/")
def index():
    status = _calculate_status(last_update_at)
    return render_template(
        "index.html",
        data=sensor_data,
        status=status,
        last_update=last_update_at.isoformat() if last_update_at else None,
        refresh_seconds=REFRESH_SECONDS,
    )


@app.route("/update", methods=["POST"])
def update():
    global sensor_data
    global last_update_at

    content = request.get_json()

    # Validate request has JSON content
    if not content:
        logger.warning("Received update request with no JSON body")
        return jsonify({"error": "Missing JSON body"}), 400

    # Validate required fields exist
    if "temperature" not in content or "humidity" not in content:
        logger.warning(f"Missing required fields in update: {content}")
        return jsonify({"error": "Missing required fields: temperature and humidity"}), 400

    # Validate and convert data types
    try:
        temp = float(content["temperature"])
        hum = float(content["humidity"])
    except (ValueError, TypeError) as e:
        logger.error(f"Invalid data types in update: {content} - {e}")
        return jsonify({"error": "Invalid data types, expected numbers"}), 400

    # Validate sensor ranges (typical for DHT11/DHT22 sensors)
    if not (-40 <= temp <= 85):
        logger.warning(f"Temperature out of range: {temp}")
        return jsonify({"error": "Temperature out of valid range (-40 to 85°C)"}), 400

    if not (0 <= hum <= 100):
        logger.warning(f"Humidity out of range: {hum}")
        return jsonify({"error": "Humidity out of valid range (0 to 100%)"}), 400

    # Update sensor data
    sensor_data["temperature"] = temp
    sensor_data["humidity"] = hum
    last_update_at = datetime.now(timezone.utc)

    logger.info(f"Sensor data updated: temp={temp}°C, humidity={hum}%")

    return jsonify(
        {
            "status": "success",
            "connection": _calculate_status(last_update_at),
            "data": sensor_data,
            "last_update": last_update_at.isoformat() if last_update_at else None,
        }
    )


@app.route("/data", methods=["GET"])
def get_data():
    return jsonify(
        {
            "data": sensor_data,
            "last_update": last_update_at.isoformat() if last_update_at else None,
            "connection": _calculate_status(last_update_at),
        }
    )


@app.route("/health", methods=["GET"])
def health():
    status = _calculate_status(last_update_at)
    now = datetime.now(timezone.utc)
    return jsonify(
        {
            "status": status,
            "data": sensor_data,
            "last_update": last_update_at.isoformat() if last_update_at else None,
            "seconds_since_update": (now - last_update_at).total_seconds()
            if last_update_at
            else None,
            "uptime_seconds": (now - app_started_at).total_seconds(),
        }
    )


if __name__ == "__main__":
    logger.info(f"Starting Flask IoT server on {HOST}:{PORT} (debug={DEBUG_MODE})")
    logger.info(f"Dashboard refresh interval: {REFRESH_SECONDS} seconds")
    app.run(host=HOST, port=PORT, debug=DEBUG_MODE)