import os

import boto3
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile

load_dotenv()

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
S3_BUCKET = os.environ["S3_BUCKET_NAME"]

_profile = os.environ.get("AWS_PROFILE")
session = boto3.Session(profile_name=_profile, region_name=AWS_REGION)
s3 = session.client("s3")

app = FastAPI()


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        s3.upload_fileobj(
            file.file,
            S3_BUCKET,
            file.filename,
            ExtraArgs={"ContentType": file.content_type},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "filename": file.filename,
        "bucket": S3_BUCKET_NAME,
        "url": f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file.filename}",
    }
