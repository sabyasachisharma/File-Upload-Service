# app/run_worker.py

import asyncio
from app.services.worker_service import worker_loop

if __name__ == "__main__":
    asyncio.run(worker_loop())
