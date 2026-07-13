import uuid
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

from app.config import *
from app.ingestion.embedding import get_embedding
from app.ingestion.chunking import chunk_text
from app.ingestion.pdf_loader import load_pdf

search_client = SearchClient(
    endpoint=SEARCH_ENDPOINT,
    index_name=INDEX_NAME,
    credential=AzureKeyCredential(SEARCH_KEY)
)

def index_text(text: str, source: str = "default_doc"):
    chunks = chunk_text(text)
    documents = []

    for chunk in chunks:
        embedding = get_embedding(chunk)

        documents.append({
            "id": str(uuid.uuid4()),
            "content": chunk,
            "embedding": embedding,
            "source": source
        })

    result = search_client.upload_documents(documents)
    return result


def index_pdf(file_path: str, source: str = "pdf_doc"):
    pages = load_pdf(file_path)

    documents = []

    for page in pages:
        chunks = chunk_text(page["text"])

        for chunk in chunks:
            embedding = get_embedding(chunk)

            documents.append({
                "id": str(uuid.uuid4()),
                "content": chunk,
                "embedding": embedding,
                "source": source,
                "page": page["page_number"]   # 🔥 VERY IMPORTANT
            })
    BATCH_SIZE = 1000

    for i in range(0, len(documents), BATCH_SIZE):
        batch = documents[i:i+BATCH_SIZE]
        search_client.upload_documents(batch)
    print(file_path, "PDF Uploaded")
    # result = search_client.upload_documents(documents)
    # return result