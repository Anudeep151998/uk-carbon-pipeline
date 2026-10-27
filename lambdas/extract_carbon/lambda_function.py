import json
import urllib.request
from datetime import datetime, timezone
import boto3

URL = "https://api.carbonintensity.org.uk/regional"
BUCKET = "anudeep-ukcarbon-raw"

s3 = boto3.client("s3")

def lambda_handler(event, context):
    # Extract: call the API (raises an error automatically on 4xx/5xx)
    with urllib.request.urlopen(URL, timeout=20) as resp:
        data = json.loads(resp.read())

    # Load: save untouched to the raw layer, partitioned by date
    run_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M")
    key = f"carbon_regional/{run_time[:10]}/regional_{run_time}.json"

    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=json.dumps(data),
        ContentType="application/json",
    )

    regions = len(data["data"][0]["regions"])
    print(f"Saved s3://{BUCKET}/{key} ({regions} regions)")
    return {"status": "ok", "key": key, "regions": regions}