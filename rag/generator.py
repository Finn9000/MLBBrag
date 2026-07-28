import os

from dotenv import load_dotenv
from openai import OpenAI

from rag.retriever import MLBBRetriever


load_dotenv()

MODEL_NAME = "gpt-5"


def create_context(results):
    """Format retrieved chunks for the LLM prompt."""
    context_parts = []

    for number, result in enumerate(results, start=1):
        context_parts.append(
            f"[Source {number} | {result['document_type']}: {result['title']}]\n"
            f"{result['chunk_text']}"
        )

    return "\n\n".join(context_parts)


def generate_answer(question, results):
    """Generate a grounded answer using only retrieved MLBB sources."""
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY is missing. Add it to your .env file.")

    client = OpenAI()
    context = create_context(results)

    instructions = """
You are an MLBB guide assistant.

Answer only using the provided sources.
If the sources do not contain enough information, say:
"I don't have enough information in the MLBB knowledge base to answer that."

Be clear and concise.
Cite factual claims using source numbers in square brackets, for example [1].
Do not invent hero statistics, item effects, builds, or patch information.
"""

    response = client.responses.create(
        model=MODEL_NAME,
        instructions=instructions,
        input=f"Question: {question}\n\nSources:\n{context}",
    )

    return response.output_text


if __name__ == "__main__":
    question = "What item gives anti-heal?"

    retriever = MLBBRetriever()
    results = retriever.search(question, top_k=8)

    answer = generate_answer(question, results)

    print(f"\nQuestion: {question}\n")
    print("Answer:")
    print(answer)