from fastapi import FastAPI
from app.api import upload
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.include_router(upload.router, prefix="/api")