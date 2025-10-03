# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Flask-based IoT monitoring dashboard for ESP32 sensor data. The system consists of:
- **Backend**: Flask server that receives sensor data via POST requests and serves a real-time dashboard
- **Frontend**: Single-page HTML dashboard with auto-refresh and connection status monitoring
- **Firmware**: ESP32/Wokwi firmware that posts temperature and humidity readings

## Architecture

### Data Flow
1. ESP32 firmware reads sensor data (temperature/humidity) and POSTs JSON to `/update`
2. Flask backend stores latest reading in memory with timestamp
3. Dashboard polls `/health` endpoint every N seconds to update UI and connection status
4. Connection status is calculated based on time elapsed since last update:
   - **connected**: ≤10 seconds since last update
   - **stale**: 10-30 seconds since last update
   - **offline**: >30 seconds or no data received

### Key Components
- **[app.py](app.py)**: Main Flask application with in-memory state management
  - `sensor_data`: Dict holding latest temperature/humidity values
  - `last_update_at`: Timestamp of most recent POST from device
  - `_calculate_status()`: Determines connection state based on thresholds
  - Endpoints: `/` (dashboard), `/update` (device POST), `/data` (GET readings), `/health` (status info)

- **[templates/index.html](templates/index.html)**: Dashboard with embedded JavaScript
  - Polls `/health` at interval defined by `STATUS_REFRESH_SECONDS`
  - Updates status badge, timestamp, and sensor values
  - Auto-refresh toggle to pause/resume polling

- **[firmware/config.h.example](firmware/config.h.example)**: Template for ESP32 Wi-Fi and API configuration
  - Students copy to `config.h` and fill in credentials
  - `POST_INTERVAL_SECONDS` should match `STATUS_REFRESH_SECONDS` for UI/firmware sync

## Development Commands

### Setup
```bash
# Create and activate virtual environment (optional but recommended)
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
# Copy .env.example to .env and adjust if needed
```

### Running the Server
```bash
python app.py
# Server starts at http://localhost:5000 (or configured FLASK_HOST:FLASK_PORT)
```

### Testing Without Hardware
```bash
# Send test data to /update endpoint
curl -X POST http://localhost:5000/update -H "Content-Type: application/json" -d '{"temperature": 23.4, "humidity": 55}'

# Check health endpoint
curl http://localhost:5000/health
```

## Configuration

### Environment Variables (.env)
- `FLASK_HOST`: Server bind address (default: 0.0.0.0)
- `FLASK_PORT`: Server port (default: 5000)
- `FLASK_DEBUG`: Debug mode (default: true)
- `STATUS_REFRESH_SECONDS`: Dashboard polling interval (default: 5)

### Firmware Configuration (firmware/config.h)
Students must create this from `config.h.example`:
- `WIFI_SSID` / `WIFI_PASSWORD`: Wi-Fi credentials
- `API_BASE_URL`: Flask server URL (use `host.docker.internal` for Wokwi)
- `POST_INTERVAL_SECONDS`: How often ESP32 sends data

## Important Notes

- **In-memory storage**: Data is not persisted; server restart clears readings
- **Single device**: Backend stores only the latest reading from any source
- **No authentication**: Educational project with no security features
- **Time zones**: All timestamps use UTC (`datetime.now(timezone.utc)`)
- **Connection thresholds**: Defined in `CONNECTED_THRESHOLD` and `STALE_THRESHOLD` constants in [app.py](app.py:29)
