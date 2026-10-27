import boto3
from botocore.exceptions import ClientError

REGION = "eu-north-1"
PREFIX = "anudeep-ukcarbon"   # bucket names must be globally unique across ALL AWS accounts
LAYERS = ["inbound", "raw", "cleaned", "rejected", "staging", "reporting"]

s3 = boto3.client("s3", region_name=REGION)

def create_bucket(name):
    try:
        s3.create_bucket(
            Bucket=name,
            CreateBucketConfiguration={"LocationConstraint": REGION},
        )
        print(f"Created:  {name}")
    except ClientError as e:
        code = e.response["Error"]["Code"]
        if code == "BucketAlreadyOwnedByYou":
            print(f"Exists:   {name} (already yours, skipping)")
        else:
            raise

if __name__ == "__main__":
    for layer in LAYERS:
        create_bucket(f"{PREFIX}-{layer}")