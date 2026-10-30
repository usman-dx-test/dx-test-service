# Weather Logger

A small command-line tool that fetches the current temperature and wind speed for a city using the free [Open-Meteo](https://open-meteo.com/) API and appends the result, with an ISO 8601 timestamp, to a local JSON log.

No API key is required.

## Prerequisites

- Python 3.8 or newer
- `pip` (Python package manager)
- An internet connection

## Installation

1. **Clone or download** this repository and open a terminal in the project folder.

2. **(Optional) Create a virtual environment:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install requests
   ```

## Usage

Run the script from the terminal:

```bash
python3 weather_logger.py
```

When prompted, enter one of the supported cities:

```
Enter a city (New York, London, Tokyo, Miami, Paris): London
London: 14.2 °C, wind 11.5 km/h
Saved to weather_history.json
```

Each run appends a new entry to `weather_history.json` in the same directory as the script.

### Supported cities

New York, London, Tokyo, Miami, Paris (case-insensitive).

## Output format

`weather_history.json` is a JSON array; each run adds one object:

```json
[
  {
    "timestamp": "2026-10-30T14:05:31.482913+00:00",
    "city": "London",
    "latitude": 51.5074,
    "longitude": -0.1278,
    "temperature_c": 14.2,
    "wind_speed_kmh": 11.5
  },
  {
    "timestamp": "2026-10-30T14:07:02.118274+00:00",
    "city": "Tokyo",
    "latitude": 35.6762,
    "longitude": 139.6503,
    "temperature_c": 19.8,
    "wind_speed_kmh": 7.3
  }
]
```

| Field            | Description                           |
| ---------------- | ------------------------------------- |
| `timestamp`      | UTC time of the reading (ISO 8601)    |
| `city`           | City name entered                     |
| `latitude`       | Latitude used for the query           |
| `longitude`      | Longitude used for the query          |
| `temperature_c`  | Current temperature in °C             |
| `wind_speed_kmh` | Current wind speed in km/h            |

## Error handling

The script exits with a non-zero status and a clear message on stderr for:

- Unsupported city names
- Network failures and timeouts
- HTTP errors or unexpected API responses
- Failures writing the log file

If `weather_history.json` is missing or corrupted, a new log is started.

## AI Code Insights daemon

This repository is monitored by the DX AI Code Insights daemon (`aicodemetricsd`). On macOS it runs as a per-user LaunchAgent, and the CLI has no `stop` command, so use `launchctl` to stop and start it.

**Stop the daemon:**

```bash
launchctl bootout gui/$(id -u)/com.getdx.aicodemetrics
aicodemetricsd status    # Service should no longer show "running"
```

While stopped, agent hooks stay installed but no sessions or commits are recorded. The LaunchAgent is still present, so the daemon starts again at the next macOS login.

**Start the daemon:**

```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.getdx.aicodemetrics.plist
aicodemetricsd status    # Service should show "running"
```

**Restart the daemon** (reloads `~/.aicodemetrics/config.json` and refreshes monitored repositories):

```bash
aicodemetricsd restart
```

To remove the daemon entirely, follow the [DX uninstallation guide](https://docs.getdx.com/ai-code-insights/uninstallation/).

## License

Provided as-is for demonstration purposes. Weather data courtesy of [Open-Meteo](https://open-meteo.com/) (CC BY 4.0).
