import boto3
from pathlib import Path

BUCKET = "anudeep-ukcarbon-raw"
LOCAL_RAW = Path("data/raw")

s3 = boto3.client("s3", region_name="eu-north-1")

def upload_all():
    files = [f for f in LOCAL_RAW.rglob("*.json")]
    for f in files:
        # Keep the same folder structure in S3, always with forward slashes
        key = f.relative_to(LOCAL_RAW).as_posix()
        s3.upload_file(str(f), BUCKET, key)
        print(f"Uploaded s3://{BUCKET}/{key}")
    print(f"Done: {len(files)} files")

if __name__ == "__main__":
    upload_all()