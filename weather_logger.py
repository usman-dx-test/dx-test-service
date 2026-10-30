#!/usr/bin/env python3
"""Fetch current weather for a city from Open-Meteo and log it to a JSON file."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

API_URL = "https://api.open-meteo.com/v1/forecast"
HISTORY_FILE = Path(__file__).with_name("weather_history.json")
REQUEST_TIMEOUT = 10  # seconds

CITIES = {
    "new york": (40.7128, -74.0060),
    "london": (51.5074, -0.1278),
    "tokyo": (35.6762, 139.6503),
    "miami": (25.7617, -80.1918),
    "paris": (48.8566, 2.3522),
}


def fetch_weather(latitude, longitude):
    """Return (temperature_c, wind_speed_kmh) for the given coordinates."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m",
    }
    response = requests.get(API_URL, params=params, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    current = response.json()["current"]
    return current["temperature_2m"], current["wind_speed_10m"]


def load_history(path):
    """Load existing log entries, or an empty list if none/unreadable."""
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        print(f"Warning: could not read {path.name}; starting a new log.", file=sys.stderr)
        return []
    return data if isinstance(data, list) else []


def save_entry(path, entry):
    """Append an entry to the JSON history file."""
    history = load_history(path)
    history.append(entry)
    with path.open("w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def main():
    supported = ", ".join(name.title() for name in CITIES)
    city_input = input(f"Enter a city ({supported}): ").strip()
    key = city_input.lower()

    if key not in CITIES:
        print(f"Unsupported city '{city_input}'. Choose one of: {supported}.", file=sys.stderr)
        return 1

    latitude, longitude = CITIES[key]

    try:
        temperature, wind_speed = fetch_weather(latitude, longitude)
    except requests.exceptions.Timeout:
        print("Error: the request to Open-Meteo timed out.", file=sys.stderr)
        return 1
    except requests.exceptions.ConnectionError:
        print("Error: network problem - could not reach Open-Meteo.", file=sys.stderr)
        return 1
    except requests.exceptions.HTTPError as e:
        print(f"Error: Open-Meteo returned an HTTP error: {e}", file=sys.stderr)
        return 1
    except requests.exceptions.RequestException as e:
        print(f"Error: request failed: {e}", file=sys.stderr)
        return 1
    except (KeyError, ValueError):
        print("Error: unexpected response format from Open-Meteo.", file=sys.stderr)
        return 1

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "city": key.title(),
        "latitude": latitude,
        "longitude": longitude,
        "temperature_c": temperature,
        "wind_speed_kmh": wind_speed,
    }

    try:
        save_entry(HISTORY_FILE, entry)
    except OSError as e:
        print(f"Error: could not write {HISTORY_FILE.name}: {e}", file=sys.stderr)
        return 1

    print(f"{entry['city']}: {temperature} °C, wind {wind_speed} km/h")
    print(f"Saved to {HISTORY_FILE.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
