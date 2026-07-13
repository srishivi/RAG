from app.llm.generator import generate_answer

def evaluate_answer(query, context, answer):
    prompt = f"""
You are an AI evaluator.

Evaluate the answer based ONLY on the provided context.

Query:
{query}

Context:
{context}

Answer:
{answer}

Evaluate on:
1. Relevance (0-10)
2. Groundedness (0-10)
3. Hallucination (Yes/No)

Return format:
Relevance: <score>
Groundedness: <score>
Hallucination: <Yes/No>
Explanation: <brief reason>
"""

    evaluation = generate_answer("Evaluate this answer", prompt)
    return evaluation