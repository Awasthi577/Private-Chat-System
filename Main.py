from fastapi import FastAPI
from .worker import start_job, shutdown_jobs

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await start_job("key_rotation", rotate_keys)
    await start_job("connection_maintainer", maintain_connection)

@app.on_event("shutdown")
async def shutdown_event():
    await shutdown_jobs()

@app.get("/")
async def root():
    return {"status": "Background jobs running"}
