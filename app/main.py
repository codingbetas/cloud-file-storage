from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.storage import generate_presigned_url
from app.kafka_producer import send_upload_event

app = FastAPI(title="Cloud File Storage")

class UploadRequest(BaseModel):
    filename: str
    file_size: int

@app.get("/")
def health():
    return {"status": "ok", "service": "Cloud File Storage"}

@app.post("/generate-upload-url")
def get_upload_url(request: UploadRequest):
    """
    Step 1: Client asks for a Presigned URL to upload their file.
    """
    # Generate the secure URL
    url = generate_presigned_url(request.filename)
    if not url:
        raise HTTPException(status_code=500, detail="Could not generate upload URL")
    
    # We immediately notify Kafka that an upload is starting
    send_upload_event(request.filename, request.file_size)
    
    return {
        "upload_url": url,
        "message": "Use this URL to PUT your file directly to S3."
    }