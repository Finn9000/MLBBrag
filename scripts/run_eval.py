import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rag.retriever import MLBBRetriever
from rag.generator import generate_answer

test_queries = [
    "What item gives anti-heal?",
    "Best build for Fanny",
    "Who counters Lancelot?",
    "What does Blade of Despair do?",
    "Which heroes are mythic tier this patch?",
    "How do I play a tank role effectively?",
    "What is the recommended emblem for mages?",
    "Tell me about the hero Gusion's skills",
    "What is the best jungle item?",
    "How do I make pizza dough?",
]

retriever = MLBBRetriever()

for q in test_queries:
    print("=" * 70)
    print("Q:", q)
    results = retriever.search(q, top_k=5)
    for i, r in enumerate(results, 1):
        print(f"  [{i}] {r['document_type']}: {r['title']} (sim={r['similarity']:.3f})")
    try:
        answer = generate_answer(q, results)
        print("ANSWER:", answer[:500])
    except Exception as e:
        print("GENERATION ERROR:", e)
    print()
