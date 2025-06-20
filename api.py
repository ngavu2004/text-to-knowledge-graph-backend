from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import asyncio
from langchain_text_splitters import RecursiveCharacterTextSplitter
from graph_functions import extract_kg_from_text
from dotenv import load_dotenv


load_dotenv()
app = FastAPI(title="Knowledge Graph API", version="1.0.0")

class TextRequest(BaseModel):
    text: str
    chunk_size: int = 2000
    chunk_overlap: int = 200

class NodeResponse(BaseModel):
    id: str
    type: str
    properties: Dict[str, Any] = {}

class RelationshipResponse(BaseModel):
    source: str
    target: str
    type: str
    properties: Dict[str, Any] = {}

class KnowledgeGraphResponse(BaseModel):
    nodes: List[NodeResponse]
    relationships: List[RelationshipResponse]
    chunks_processed: int

@app.post("/extract-kg", response_model=KnowledgeGraphResponse)
async def extract_knowledge_graph(request: TextRequest):
    """
    Extract knowledge graph from text by chunking and processing each chunk
    """
    try:
        nodes, relationships = await extract_kg_from_text(request.text)
        
        # Convert the tuples to dictionaries for the response model
        node_responses = []
        for node_id, node_type in nodes:
            node_responses.append(NodeResponse(id=node_id, type=node_type))
            
        relationship_responses = []
        for source, target, rel_type in relationships:
            relationship_responses.append(RelationshipResponse(source=source, target=target, type=rel_type))
        
        return KnowledgeGraphResponse(
            nodes=node_responses,
            relationships=relationship_responses,
            chunks_processed=len(request.text.split())  # Approximate chunk count
        )
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing knowledge graph: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)