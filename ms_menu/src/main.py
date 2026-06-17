from fastapi import FastAPI
from src.api.routes.position_routes import router as position_router
from src.api.routes.super_position_routes import router as super_position_router

app = FastAPI()
app.include_router(position_router, prefix="/menu")
app.include_router(super_position_router, prefix="/menu")

@app.get("/health")
async def health():
    return {"status": "ok"}