from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Knowledge Graph API",
    version="1.0.0",
    docs_url="/"  # Redirect root path to Swagger docs
)
app.include_router(router)
