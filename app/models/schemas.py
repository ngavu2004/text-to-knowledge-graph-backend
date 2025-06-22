from pydantic import BaseModel

class TextRequest(BaseModel):
    text: str
    chunk_size: int = 2000
    chunk_overlap: int = 200