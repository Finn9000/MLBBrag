from pathlib import Path

import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer


PROJECT_DIR = Path(__file__).resolve().parent.parent
CHUNKS_PATH = PROJECT_DIR / "data" / "mlbb_chunks.csv"
INDEX_PATH = PROJECT_DIR / "vector_db" / "mlbb_index.faiss"

MODEL_NAME = "all-MiniLM-L6-v2"


class MLBBRetriever:
    def __init__(self):
        self.chunks_df = pd.read_csv(CHUNKS_PATH)
        self.index = faiss.read_index(str(INDEX_PATH))
        self.model = SentenceTransformer(MODEL_NAME)

    def search(self, question, top_k=5):
        """Return the most relevant chunks for a user question."""
        question_embedding = self.model.encode(
            [question],
            normalize_embeddings=True,
        )

        scores, indices = self.index.search(question_embedding, top_k)

        results = []

        for score, index in zip(scores[0], indices[0]):
            chunk = self.chunks_df.iloc[index]

            results.append(
                {
                    "title": chunk["title"],
                    "document_type": chunk["document_type"],
                    "chunk_text": chunk["chunk_text"],
                    "similarity": float(score),
                }
            )

        return results


if __name__ == "__main__":
    retriever = MLBBRetriever()

    question = "What item gives anti-heal?"
    results = retriever.search(question, top_k=5)

    print(f"\nQuestion: {question}\n")

    for number, result in enumerate(results, start=1):
        print(f"{number}. {result['document_type']}: {result['title']}")
        print(f"Similarity: {result['similarity']:.3f}")
        print(f"Text: {result['chunk_text'][:400]}...")
        print("-" * 70)