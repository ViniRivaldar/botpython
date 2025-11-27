# main.py
import os
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from db import fetch_audit_logs

load_dotenv()
app = FastAPI(title="Audit JSON API")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/audit_logs")
async def audit_logs(
    limit: int = Query(100, ge=1, le=5000),
    since_id: int | None = Query(None),
):
    logs = await fetch_audit_logs(limit=limit, since_id=since_id)
    return JSONResponse(logs)
