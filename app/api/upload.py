from fastapi import APIRouter, HTTPException, Depends, Security
from uuid import uuid4
import logging
from pydantic import BaseModel 
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKeyHeader

from app.core.config import API_KEY
from app.services.storage_service import upload_file_to_s3
from app.services.queue_service import publish_to_queue
from app.services.database_service import save_upload_metadata
from app.services.preprocessing_service import preprocess_file

logger = logging.getLogger(__name__)

router = APIRouter()
api_key_header = APIKeyHeader(name="access_token", auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

class UploadRequest(BaseModel):
    user_id: str
    file_name: str

@router.post("/upload")
async def upload_file(request: UploadRequest, api_key: str = Depends(get_api_key)):
    try:
        logger.info(f"Received upload request for user_id={request.user_id}, file_name={request.file_name}")
        upload_id = str(uuid4())
        s3_key = f"uploads/{upload_id}/{request.file_name}"

        await upload_file_to_s3(s3_key)
        await save_upload_metadata(upload_id, request.user_id, s3_key)
        await publish_to_queue(upload_id, s3_key, request.user_id)

        preprocess_result = await preprocess_file(upload_id, s3_key)
        logger.info(f"Preprocessing result: {preprocess_result}")

        return JSONResponse(
            status_code=202,
            content={
                "upload_id": upload_id,
                "status": "pending",
                "message": "Upload received. Processing started."
            }
        )
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/health")
async def health_check():
    return {"status": "healthy"}