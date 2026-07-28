import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rag.retriever import MLBBRetriever

r = MLBBRetriever()
for q in ["Which heroes are SS tier this patch?", "What is Gloo's tier and role?"]:
    print("Q:", q)
    res = r.search(q, top_k=5)
    for x in res:
        print(" ", x['document_type'], x['title'], round(x['similarity'], 3))
    print()
