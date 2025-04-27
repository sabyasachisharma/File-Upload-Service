# FastAPI Upload Service

A File Upload service using **FastAPI** that allows users to upload files, tracks their processing status, and queues jobs for downstream processing. 
---

## Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/fastapi-upload-service.git
cd fastapi-upload-service
```

### 2. Choose Setup Method

#### A. Using Docker (Recommended)
```bash
# Build the Docker image
docker build -t fastapi-upload-service .

# Run the container
docker run -p 8000:8000 fastapi-upload-service
```

#### B. Manual Setup
```bash
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Running the Worker Service
The service includes a background worker that processes uploaded files. The worker:
- Polls the queue for new upload jobs
- Downloads files from S3
- Sends them through preprocessing
- Updates job status in the database

To run the worker:
```bash
# Using Docker
docker run fastapi-upload-service python -m app.worker

# Manual Setup
python -m app.worker
```

### 4. Running Tests
```bash
# Run tests
python -m pytest -v

# Run specific test
python -m pytest tests/test_upload.py -k test_health_check -v
```

- Open API Docs: `http://localhost:8000/docs`

---

## 🔍 API Endpoints

### POST `/api/upload`
Initiates a file upload process. The file will be processed asynchronously by the worker service.

**Headers:**
- `access_token: supersecretapikey123`

**Request Body:**
```json
{
  "user_id": "abc123",
  "file_name": "document.pdf"
}
```

**Response:**
```json
{
  "upload_id": "xyz789",
  "status": "pending",
  "message": "Upload received. Processing started."
}
```

### GET `/api/health`
Returns the health status of the service.

**Response:**
```json
{
  "status": "healthy"
}
```
