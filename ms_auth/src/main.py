from fastapi import FastAPI
from src.api.routes.auth_routes import router as auth_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])


@app.get("/health")
async def health():
    return {"status": "ok"}
