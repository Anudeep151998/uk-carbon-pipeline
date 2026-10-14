import requests
import json
from datetime import datetime, timezone
from pathlib import Path
from regions import REGIONS

URL = "https://api.open-meteo.com/v1/forecast"

def extract():
    # One API call for all 14 locations: Open-Meteo accepts comma-separated coordinates
    params = {
        "latitude":  ",".join(str(r["lat"]) for r in REGIONS),
        "longitude": ",".join(str(r["lon"]) for r in REGIONS),
        "hourly": "temperature_2m,wind_speed_10m,cloud_cover,shortwave_radiation",
        "forecast_days": 1,
        "timezone": "UTC",
    }
    response = requests.get(URL, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    # Tag each result with its region so it can be joined to carbon data later
    for region, result in zip(REGIONS, data):
        result["regionid"] = region["regionid"]
        result["city"] = region["city"]

    run_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M")
    out_dir = Path("data/raw/weather_hourly") / run_time[:10]
    out_dir.mkdir(parents=True, exist_ok=True)

    out_file = out_dir / f"weather_{run_time}.json"
    out_file.write_text(json.dumps(data, indent=2))
    print(f"Saved {out_file} ({len(data)} locations)")

if __name__ == "__main__":
    extract()