from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.llm_provider import llm_transformer

class KGRepository:
    def __init__(self, chunk_size=2000, chunk_overlap=200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    async def extract_from_text(self, text: str):
        chunks = self.splitter.split_text(text)

        all_nodes = []
        all_relationships = []

        for chunk in chunks:
            doc = Document(page_content=chunk)
            graph_doc = await llm_transformer.aconvert_to_graph_documents([doc])
            all_nodes.extend(graph_doc[0].nodes)
            all_relationships.extend(graph_doc[0].relationships)

        return (
            [(n.id, n.type) for n in all_nodes],
            [(r.source.id, r.target.id, r.type) for r in all_relationships]
        )
