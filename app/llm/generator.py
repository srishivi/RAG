from openai import AzureOpenAI
from app.config import *

client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

# SYSTEM_PROMPT = (
#     "You are a helpful assistant. "
#     "Answer ONLY from the provided context. "
#     "If the answer is not present, say 'I don’t know'."
# )





def generate_answer(query: str, context: str):
    SYSTEM_PROMPT = f"""
    You are a helpful AI assistant.

    Answer the question ONLY using the provided context.

    STRICT RULES:
    - Do NOT use external knowledge
    - Do NOT make assumptions
    - If answer is not in context, say: "I don't know based on the document"
    - ALWAYS include citations using chunk numbers like [1], [2]

    Context:
    {context}

    Question:
    {query}

    Return format:

    Answer:
    <your answer with citations like [1], [2]>

    Sources:
    [1]: <short quote from chunk 1>
    [2]: <short quote from chunk 2>
    """
    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
        ]
    )

    return response.choices[0].message.content