from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import TextRequest
from app.services.kg_service import KGService
from app.repositories.kg_repository import KGRepository
from app.models.domain import KnowledgeGraphResponse
import pdfplumber

router = APIRouter()
kg_service = KGService(KGRepository())

@router.post("/extract-kg")
async def extract_kg(request: TextRequest):
    try:
        return await kg_service.extract_graph(request.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def extract_text_from_pdf(file: UploadFile) -> str:
    try:
        with pdfplumber.open(file.file) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to read PDF content")

@router.post("/upload", response_model=KnowledgeGraphResponse)
async def upload_file(file: UploadFile = File(...)):
    try:
        if file.filename.endswith(".pdf"):
            text = await extract_text_from_pdf(file)
        elif file.filename.endswith((".txt", ".md")):
            content = await file.read()
            text = content.decode("utf-8")
        else:
            raise HTTPException(status_code=400, detail="Only .txt, .md, and .pdf files are supported.")

        return await kg_service.extract_graph(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health():
    return {"status": "healthy"}
