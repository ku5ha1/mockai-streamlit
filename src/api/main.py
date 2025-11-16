from fastapi import FastAPI
from src.core.database import Base, engine
from src.api.routes.auth import router as auth_router

app = FastAPI()

def init_db():
    Base.metadata.create_all(bind=engine)
    
app.include_router(auth_router)
    
@app.get("/healthz")
async def get_health():
    return {"message": "Server running successfully"}

@app.on_event("startup")
async def startup_event():
    init_db()