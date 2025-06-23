from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_experimental.graph_transformers import LLMGraphTransformer
from app.core.config import settings

load_dotenv()
llm = ChatOpenAI(
    temperature=0,
    model_name="gpt-4.1-nano",
    api_key=settings.OPENAI_API_KEY
)
llm_transformer = LLMGraphTransformer(llm=llm)
