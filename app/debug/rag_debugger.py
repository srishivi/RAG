def debug_retrieval(query, retrieved_chunks):
    print("\n" + "="*60)
    print("🔍 RAG DEBUGGER")
    print("="*60)

    print(f"\n🧠 Query: {query}\n")

    for i, chunk in enumerate(retrieved_chunks):
        print(f"--- Chunk {i+1} ---")
        print(f"📄 Page: {chunk.get('page', 'N/A')}")
        
        if "score" in chunk:
            print(f"📊 Score: {chunk['score']}")
        if "rerank_score" in chunk:
            print(f"🔁 Rerank Score: {chunk['rerank_score']}")
        
        print(f"📝 Content Preview:\n{chunk['content'][:300]}")
        print("-"*40)

    print("\n✅ Retrieval Debug Complete\n")