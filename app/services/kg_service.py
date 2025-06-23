from app.repositories.kg_repository import KGRepository
from app.models.domain import NodeResponse, RelationshipResponse, KnowledgeGraphResponse

class KGService:
    def __init__(self, kg_repo: KGRepository):
        self.kg_repo = kg_repo

    async def extract_graph(self, text: str):
        nodes, relationships = await self.kg_repo.extract_from_text(text)

        node_responses = [NodeResponse(id=n[0], type=n[1]) for n in nodes]
        relationship_responses = [RelationshipResponse(source=r[0], target=r[1], type=r[2]) for r in relationships]

        return KnowledgeGraphResponse(
            nodes=node_responses,
            relationships=relationship_responses,
            chunks_processed=len(text.split())
        )
