from fastapi import FastAPI
from src.routes.routes import router as root_router

app = FastAPI()
app.include_router(root_router)