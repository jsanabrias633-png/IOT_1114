import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from dotenv import load_dotenv
from flask import Flask, request, render_template, jsonify

load_dotenv()

app = Flask(__name__)


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
    if content:
        sensor_data["temperature"] = content.get("temperature")
        sensor_data["humidity"] = content.get("humidity")
        last_update_at = datetime.now(timezone.utc)

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
    app.run(host=HOST, port=PORT, debug=DEBUG_MODE)