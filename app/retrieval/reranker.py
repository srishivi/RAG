from app.llm.generator import generate_answer
import re
def rerank_chunks(query, chunks, top_n=5):
    scored_chunks = []

    for chunk in chunks:
        prompt = f"""
You are a relevance scoring assistant.

Query:
{query}

Chunk:
{chunk['content']}

Score relevance from 0 to 10.

STRICT RULES:
- Return ONLY a number
- Do NOT include text
- Do NOT explain
- Example outputs: 0, 5, 8, 10

Score:
"""

        try:
            score = generate_answer("score", prompt)
            # print("RAW SCORE:", score)
            match = re.search(r"\d+(\.\d+)?", score)
            score = float(match.group()) if match else 0
        except:
            score = 0
        
        chunk["rerank_score"] = score
        scored_chunks.append(chunk)

    # Sort by score descending
    ranked = sorted(scored_chunks, key=lambda x: x["rerank_score"], reverse=True)

    return ranked[:top_n]