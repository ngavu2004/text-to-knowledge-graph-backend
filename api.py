from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import asyncio
from langchain_text_splitters import RecursiveCharacterTextSplitter
from graph_functions import extract_kg_from_text
import os

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
        # 1. Split text into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap
        )
        chunks = splitter.split_text(request.text)
        
        if not chunks:
            raise HTTPException(status_code=400, detail="No text chunks created")
        
        # 2. Process each chunk
        all_nodes = []
        all_relationships = []
        
        for chunk in chunks:
            try:
                nodes, relationships = await extract_kg_from_text(chunk)
                all_nodes.extend(nodes)
                all_relationships.extend(relationships)
            except Exception as e:
                print(f"Error processing chunk: {e}")
                continue
        
        # 3. Deduplicate nodes and relationships
        unique_nodes = {}
        for node in all_nodes:
            key = (node.id, node.type)
            if key not in unique_nodes:
                unique_nodes[key] = NodeResponse(
                    id=node.id,
                    type=node.type,
                    properties=getattr(node, 'properties', {})
                )
        
        unique_relationships = {}
        for rel in all_relationships:
            key = (rel.source.id, rel.target.id, rel.type)
            if key not in unique_relationships:
                unique_relationships[key] = RelationshipResponse(
                    source=rel.source.id,
                    target=rel.target.id,
                    type=rel.type,
                    properties=getattr(rel, 'properties', {})
                )
        
        return KnowledgeGraphResponse(
            nodes=list(unique_nodes.values()),
            relationships=list(unique_relationships.values()),
            chunks_processed=len(chunks)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)