from pathlib import Path

import faiss
import numpy as np


PROJECT_DIR = Path(__file__).resolve().parent.parent
VECTOR_DB_DIR = PROJECT_DIR / "vector_db"

EMBEDDINGS_PATH = VECTOR_DB_DIR / "chunk_embeddings.npy"
INDEX_PATH = VECTOR_DB_DIR / "mlbb_index.faiss"


def create_faiss_index():
    """Create a FAISS index for cosine-similarity search."""
    embeddings = np.load(EMBEDDINGS_PATH).astype("float32")

    # The embeddings were normalized earlier, so inner product = cosine similarity.
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, str(INDEX_PATH))

    print(f"FAISS index created with {index.ntotal} vectors.")
    print(f"Saved index to: {INDEX_PATH}")


if __name__ == "__main__":
    create_faiss_index()