from fastapi import APIRouter, UploadFile, File
import shutil
import os

from app.ingestion.pdf_loader import load_pdf
from app.ingestion.indexer import index_text

from app.retrieval.retriever import retrieve
from app.retrieval.reranker import rerank_chunks

from app.llm.generator import generate_answer
from app.evaluation.evaluator import evaluate_answer
from app.guard.hallucination_guard import apply_hallucination_guard
from app.debug.rag_debugger import debug_retrieval

router = APIRouter()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# 🚀 1. Upload Endpoint
@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract + index
    text = load_pdf(file_path)
    index_text(text)

    return {
        "message": f"{file.filename} uploaded and indexed successfully"
    }


# 🚀 2. Ask Endpoint
@router.post("/ask")
async def ask_question(query: str):
    # 🔍 Retrieve
    results = retrieve(query)

    # 🧠 Rerank
    retrieved_chunks = rerank_chunks(query, results)
  

       # Step 2: Debug
    debug_retrieval(query, retrieved_chunks)
    
    print(f"Retrieved Chunks: {retrieved_chunks}")
    

    # Step 3: Build context
    context_items = []
    for i, c in enumerate(retrieved_chunks):
        context_items.append(
            f"[{i+1}] (Page {c['page']}) {c['content']}"
        )

    context = "\n\n".join(context_items)

    # 🤖 Generate answer
    answer = generate_answer(query, context)

    # 🧪 Evaluate
    evaluation = evaluate_answer(query, context, answer)

    # 🛡️ Guard
    guard_result = apply_hallucination_guard(answer, evaluation)

    return {
        "query": query,
        "answer": guard_result["answer"],
        "status": guard_result["status"],
        "reason": guard_result["reason"],
        "evaluation": evaluation,
        "sources": [
            {
                "content": doc["content"][:200],
                "score": doc.get("@search.score", None),
                "rerank_score": doc.get("@search.reranker_score", None),
            }
            for doc in retrieved_chunks
        ]
    }