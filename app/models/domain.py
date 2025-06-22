from pydantic import BaseModel
from typing import Dict, List, Any

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
