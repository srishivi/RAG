from app.ingestion.indexer import index_text, index_pdf
from app.retrieval.retriever import retrieve
from app.llm.generator import generate_answer
from app.utils.logger import log
from pathlib import Path

from app.debug.rag_debugger import debug_retrieval
from app.evaluation.evaluator import evaluate_answer
from app.retrieval.reranker import rerank_chunks

from app.utils.logger import setup_logging
from app.guard.hallucination_guard import apply_hallucination_guard
from fastapi import FastAPI
from app.api.routes import router

setup_logging()
app = FastAPI(title="RAG API", version="1.0")

app.include_router(router)

def run_pipeline():
    text = """
    Azure AI Search enables vector search and semantic ranking.
    It is used in RAG applications to retrieve relevant documents.
    """

    # Step 1: Index
    # index_text(text, source="sample_doc")

    BASE_DIR = Path(__file__).resolve().parent.parent  # goes to project root

    pdf_path = BASE_DIR / "data" / "documents" / "ShivaniSrivastava_Gen_AI_Engineer.pdf"

    # index_pdf(str(pdf_path))

    # Step 2: Query
    query = "What is the summary of '1-2+Simple+RNN.pdf pdf"

    log(f"Query: {query}")

    # Step 1: Retrieve
    retrieved_chunks = retrieve(query, k=10)

    # Step 2: Rerank
    retrieved_chunks = rerank_chunks(query, retrieved_chunks, top_n=5)

    # Step 2: Debug
    debug_retrieval(query, retrieved_chunks)

    log(f"Retrieved Chunks: {retrieved_chunks}")

    # Step 3: Build context
    context_items = []
    for i, c in enumerate(retrieved_chunks):
        context_items.append(
            f"[{i+1}] (Page {c['page']}) {c['content']}"
        )

    context = "\n\n".join(context_items)

    # Step 4: Generate Answer
    answer = generate_answer(query, context)

    print("\n🤖 Answer:\n", answer)

    # Step 5: Evaluate
    evaluation = evaluate_answer(query, context, answer)

    print("\n🧪 Evaluation:\n")
    print(evaluation)

    # 🛡️ Apply guard
    guard_result = apply_hallucination_guard(answer, evaluation)

    print("\n🛡️ Guard Result:\n")
    print("Status:", guard_result["status"])
    print("Reason:", guard_result["reason"])

    print("\n✅ Final Output:\n")
    print(guard_result["answer"])

if __name__ == "__main__":
    run_pipeline()