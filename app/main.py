# app/main.py
from fastapi import FastAPI
from features import feature_routers
from db.database import test_db_connection

app = FastAPI(
    title="AI Resume Builder",
    description="An intelligent resume builder application",
    version="1.0.0"
)

# Include all feature routers
for router in feature_routers:
    app.include_router(router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "AI Resume Builder is up and running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "ai-resume-builder"}

@app.on_event("startup")
async def startup_event():
     test_db_connection()