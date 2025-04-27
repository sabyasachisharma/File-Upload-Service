async def save_upload_metadata(upload_id: str, user_id: str, s3_key: str):
    # Stub: Pretend to save metadata to a database
    pass

async def update_job_status(upload_id: str, status: str):
    # Stub: Update the status of the job in the database to 'completed'
    pass

async def mark_job_as_failed(upload_id: str, error: str):
    # Stub: Update the status of the job in the database to 'failed' and save error message
    pass
