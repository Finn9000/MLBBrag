import pandas as pd

from loader import load_knowledge_base


def split_into_chunks(text, chunk_size=200, overlap=40):
    """Split text into overlapping chunks measured in words."""
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def create_chunks(knowledge_base):
    """Create a table where each row is one chunk."""
    chunk_rows = []

    for _, document in knowledge_base.iterrows():
        chunks = split_into_chunks(document["document"])

        for chunk_number, chunk_text in enumerate(chunks, start=1):
            chunk_rows.append(
                {
                    "document_id": document["document_id"],
                    "chunk_number": chunk_number,
                    "title": document["title"],
                    "document_type": document["document_type"],
                    "chunk_text": chunk_text,
                }
            )

    chunks_df = pd.DataFrame(chunk_rows)
    chunks_df.insert(0, "chunk_id", range(1, len(chunks_df) + 1))

    return chunks_df


if __name__ == "__main__":
    knowledge_base = load_knowledge_base()
    chunks_df = create_chunks(knowledge_base)

    chunks_df.to_csv("data/mlbb_chunks.csv", index=False)

    print(f"Created {len(chunks_df)} chunks.")
    print(chunks_df[["chunk_id", "title", "document_type"]].head())