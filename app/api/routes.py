from fastapi import APIRouter, HTTPException
from app.models.schemas import TextRequest
from app.services.kg_service import KGService
from app.repositories.kg_repository import KGRepository

router = APIRouter()
kg_service = KGService(KGRepository())

@router.post("/extract-kg")
async def extract_kg(request: TextRequest):
    try:
        return await kg_service.extract_graph(request.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health():
    return {"status": "healthy"}
