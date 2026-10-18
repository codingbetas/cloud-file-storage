# Cloud File Storage (AWS S3 Clone)

A scalable, cloud-native file storage API inspired by AWS S3 and Google Drive. This project demonstrates how to handle massive file uploads without overloading the API server, using Object Storage and Event Streaming.

## 🧠 System Design Concepts Demonstrated

1. **Presigned URLs:** The API does not handle file uploads. Instead, it generates a secure, time-limited URL (using `boto3`). The client uploads the file *directly* to the object storage (MinIO), saving API bandwidth and preventing crashes.
2. **Object Storage (MinIO):** Uses MinIO, an open-source S3-compatible storage system. Files are organized into buckets, just like in AWS.
3. **Event Streaming (Kafka):** When an upload is initiated, a message is produced to an Apache Kafka topic. This allows decoupled background workers to process the file (e.g., virus scanning, thumbnail generation) asynchronously.
4. **Direct-to-Cloud Uploads:** Bypasses the backend entirely, which is essential for large files (like 100MB videos).

## 🏗️ Architecture

```text
       ┌──────────────┐
       │    Client    │
       └──────┬───────┘
              │ 1. POST /generate-upload-url
              ▼
       ┌──────────────┐     2. Send Event         ┌──────────────┐
       │   FastAPI    │──────────────────────────▶│    Kafka     │
       └──────┬───────┘                           └──────────────┘
              │ 3. Return Presigned URL
              ▼
       ┌──────────────┐
       │    Client    │
       └──────┬───────┘
              │ 4. PUT File (Direct Upload)
              ▼
       ┌──────────────┐
       │    MinIO     │ (S3-Compatible Object Storage)
       └──────────────┘
```

## 🛠️ Tech Stack

- **API:** FastAPI, Python 3.12
- **Object Storage:** MinIO (S3-Compatible)
- **Message Broker:** Apache Kafka
- **Orchestration:** Docker Compose
- **AWS SDK:** `boto3`

## 🚀 How to Run

**1. Start the infrastructure (MinIO, Kafka, Zookeeper):**
```bash
docker compose up -d
```

**2. Create the bucket in MinIO:**
- Open `http://localhost:9001` in your browser.
- Login with Username: `admin` and Password: `password123`.
- Create a bucket named `uploads`.

**3. Install dependencies and start the API:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**4. Test it:**
- Go to `http://localhost:8000/docs`.
- Use `POST /generate-upload-url` to get a presigned URL.
- Upload a file directly to that URL using `curl`:
  ```bash
  curl -X PUT "YOUR_PRESIGNED_URL" -d "This is a test file"
  ```
- Check the MinIO console (`http://localhost:9001`) to see the file in the `uploads` bucket!

## 📄 License

MIT