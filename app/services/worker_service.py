# app/services/worker_service.py

import asyncio
import logging
from app.services.queue_service import fetch_job_from_queue, delete_job_from_queue
from app.services.storage_service import download_file_from_storage, upload_processed_data
from app.services.preprocessing_service import send_to_preprocessing_black_box
from app.services.database_service import update_job_status, mark_job_as_failed

logger = logging.getLogger(__name__)

async def worker_loop():
    while True:
        logger.info("Polling for new jobs...")
        job = await fetch_job_from_queue()

        if not job:
            logger.info("No jobs found. Sleeping for 5 seconds...")
            await asyncio.sleep(5)
            continue

        try:
            logger.info(f"Processing job {job['upload_id']}")

            # Download the raw file
            file_data = await download_file_from_storage(job['s3_key'])

            # Send to Preprocessing Black Box
            processed_data = await send_to_preprocessing_black_box(file_data)

            # Upload processed data
            await upload_processed_data(job['upload_id'], processed_data)

            # Update job status to completed
            await update_job_status(job['upload_id'], status="completed")

            # Delete job from queue
            await delete_job_from_queue(job['receipt_handle'])

            logger.info(f"Successfully processed job {job['upload_id']}")

        except Exception as e:
            logger.error(f"Failed to process job {job['upload_id']}: {str(e)}")
            await mark_job_as_failed(job['upload_id'], error=str(e))

        await asyncio.sleep(1)
