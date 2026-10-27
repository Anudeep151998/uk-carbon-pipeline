import json
import urllib.request
import urllib.parse
from datetime import datetime, timezone
import boto3

URL = "https://api.open-meteo.com/v1/forecast"
BUCKET = "anudeep-ukcarbon-raw"

# Reference data: one representative city per Carbon Intensity region (IDs 1-14)
REGIONS = [
    {"regionid": 1,  "city": "Inverness",   "lat": 57.48, "lon": -4.22},
    {"regionid": 2,  "city": "Glasgow",     "lat": 55.86, "lon": -4.25},
    {"regionid": 3,  "city": "Manchester",  "lat": 53.48, "lon": -2.24},
    {"regionid": 4,  "city": "Newcastle",   "lat": 54.98, "lon": -1.61},
    {"regionid": 5,  "city": "Leeds",       "lat": 53.80, "lon": -1.55},
    {"regionid": 6,  "city": "Liverpool",   "lat": 53.41, "lon": -2.98},
    {"regionid": 7,  "city": "Cardiff",     "lat": 51.48, "lon": -3.18},
    {"regionid": 8,  "city": "Birmingham",  "lat": 52.49, "lon": -1.89},
    {"regionid": 9,  "city": "Nottingham",  "lat": 52.95, "lon": -1.15},
    {"regionid": 10, "city": "Norwich",     "lat": 52.63, "lon": 1.30},
    {"regionid": 11, "city": "Exeter",      "lat": 50.72, "lon": -3.53},
    {"regionid": 12, "city": "Southampton", "lat": 50.90, "lon": -1.40},
    {"regionid": 13, "city": "London",      "lat": 51.51, "lon": -0.13},
    {"regionid": 14, "city": "Maidstone",   "lat": 51.27, "lon": 0.52},
]

s3 = boto3.client("s3")

def lambda_handler(event, context):
    params = urllib.parse.urlencode({
        "latitude":  ",".join(str(r["lat"]) for r in REGIONS),
        "longitude": ",".join(str(r["lon"]) for r in REGIONS),
        "hourly": "temperature_2m,wind_speed_10m,cloud_cover,shortwave_radiation",
        "forecast_days": 1,
        "timezone": "UTC",
    })
    with urllib.request.urlopen(f"{URL}?{params}", timeout=20) as resp:
        data = json.loads(resp.read())

    # Attach our own join key (never join on lat/lon: the API snaps to a grid)
    for region, result in zip(REGIONS, data):
        result["regionid"] = region["regionid"]
        result["city"] = region["city"]

    run_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M")
    key = f"weather_hourly/{run_time[:10]}/weather_{run_time}.json"

    s3.put_object(Bucket=BUCKET, Key=key, Body=json.dumps(data),
                  ContentType="application/json")

    print(f"Saved s3://{BUCKET}/{key} ({len(data)} locations)")
    return {"status": "ok", "key": key, "locations": len(data)}