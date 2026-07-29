import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"C:\Users\DELL\Desktop\MLBB-RAG")

from rag.retriever import MLBBRetriever
from rag.generator import generate_answer

q = "How do I build Ling?"

retriever = MLBBRetriever()
results = retriever.search(q, top_k=5)
top = results[0]

print(f"TOP_SOURCE: {top['document_type']}: {top['title']}")
print(f"SIMILARITY: {top['similarity']:.3f}")
print("ALL_SOURCES:")
for r in results:
    print(f"  {r['document_type']}: {r['title']} ({r['similarity']:.3f})")

answer = generate_answer(q, results)
print("ANSWER:")
print(answer)

print("\nCONTAINS 'Starlium':", "Starlium" in answer)
print("CONTAINS 'Divine Glaive':", "Divine Glaive" in answer)
