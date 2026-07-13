from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from azure.core.credentials import AzureKeyCredential

from app.config import *
from app.ingestion.embedding import get_embedding

search_client = SearchClient(
    endpoint=SEARCH_ENDPOINT,
    index_name=INDEX_NAME,
    credential=AzureKeyCredential(SEARCH_KEY)
)

def retrieve(query: str, k: int = 5):
    query_embedding = get_embedding(query)

    vector_query = VectorizedQuery(
        vector=query_embedding,
        k_nearest_neighbors=k,
        fields="embedding"
    )

    results = search_client.search(
        search_text=query,
        vector_queries=[vector_query],
        top = k,
        select=["content", "page", "source"]
    )

    chunks = []
    for result in results:
        chunks.append({
            "content": result["content"],
            "page": result.get("page"),
            "source": result.get("source",0),
            "score": result.get("@search.score",0)
        })
    return chunks