import requests
import json
from datetime import datetime, timezone
from pathlib import Path

URL = "https://api.carbonintensity.org.uk/regional"

def extract():
    response = requests.get(URL, timeout=30)
    response.raise_for_status()          # stop with an error if the API fails
    data = response.json()

    run_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M")
    out_dir = Path("data/raw/carbon_regional") / run_time[:10]   # one folder per date
    out_dir.mkdir(parents=True, exist_ok=True)

    out_file = out_dir / f"regional_{run_time}.json"
    out_file.write_text(json.dumps(data, indent=2))
    print(f"Saved {out_file}")

if __name__ == "__main__":
    extract()