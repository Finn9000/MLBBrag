from pathlib import Path

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer


PROJECT_DIR = Path(__file__).resolve().parent.parent
CHUNKS_PATH = PROJECT_DIR / "data" / "mlbb_chunks.csv"
VECTOR_DB_DIR = PROJECT_DIR / "vector_db"

MODEL_NAME = "all-MiniLM-L6-v2"


def create_embeddings():
    """Create and save normalized embeddings for every MLBB text chunk."""
    chunks_df = pd.read_csv(CHUNKS_PATH)

    model = SentenceTransformer(MODEL_NAME)

    embeddings = model.encode(
        chunks_df["chunk_text"].tolist(),
        show_progress_bar=True,
        normalize_embeddings=True,
    )

    VECTOR_DB_DIR.mkdir(exist_ok=True)
    output_path = VECTOR_DB_DIR / "chunk_embeddings.npy"
    np.save(output_path, embeddings)

    print(f"Created {len(embeddings)} embeddings.")
    print(f"Embedding shape: {embeddings.shape}")
    print(f"Saved embeddings to: {output_path}")


if __name__ == "__main__":
    create_embeddings()