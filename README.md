# MLBB RAG Search System

A Retrieval-Augmented Generation (RAG) search system for Mobile Legends: Bang Bang
(MLBB), built for CS382 Final Project. Ask natural-language questions about heroes,
items, and the current tier list, and get grounded answers with visible citations
back to the source chunks.

## Architecture

```
Ingest & Chunk  ->  Embed  ->  Vector Store (FAISS)  ->  Retrieve  ->  Generate (LLM)  ->  Interface
```

| Stage         | File                    | What it does                                                    |
|---------------|-------------------------|-------------------------------------------------------------------|
| Ingest        | `rag/loader.py`         | Loads heroes, items, and tier-list CSVs into one knowledge base   |
| Chunk         | `rag/chunker.py`        | Splits each document into retrievable chunks                     |
| Embed         | `rag/embedder.py`       | Encodes chunks with `sentence-transformers/all-MiniLM-L6-v2`      |
| Index         | `rag/vector_store.py`   | Builds a FAISS index over the chunk embeddings                   |
| Retrieve      | `rag/retriever.py`      | Embeds the query and returns top-k most similar chunks           |
| Generate      | `rag/generator.py`      | Passes query + chunks to an LLM for a grounded, cited answer      |
| Interface     | `app.py`                | Streamlit UI: query box, top-k slider, answer, sources, hero card|

## Data Sources

- `data/mlbb_heroes_cleaned.csv` — per-hero guides (builds, emblems, skills, counters)
- `data/mlbb_items_cleaned.csv` — item stats and use cases
- `data/mlbb_tierlist_mythic_2026-07-27.csv` — current Mythic-rank tier list (133 heroes)

## Setup

1. Create and activate a virtual environment, then install dependencies:
   ```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Add your OpenAI API key to a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your-key-here
   ```
3. Build the knowledge base (run once, or after editing any data file):
   ```
   python rag\chunker.py
   python rag\embedder.py
   python rag\vector_store.py
   ```
4. Launch the app:
   ```
   python -m streamlit run app.py
   ```
   (Use `python -m streamlit` rather than `streamlit.exe` directly — some
   Windows Application Control policies block the unsigned executable.)

## Features

- **Grounded Q&A** with visible source citations and similarity scores.
- **Graceful failure**: out-of-domain questions (e.g. "how do I make pizza dough?")
  return "I don't have enough information" instead of a hallucinated answer.
- **Adjustable Top-K** retrieval via a sidebar slider.
- **Hero cards**: when a question mentions a specific hero by name, the app
  displays that hero's portrait, role, and an expandable skill breakdown
  (passive, skills, ultimate) pulled directly from the source data.

## Known Limitations

- **Source data quality**: the scraped hero guides occasionally contained
  outdated or incorrect build recommendations (e.g. an early version of the
  Ling entry recommended `Starlium Scythe` and `Divine Glaive`, neither of
  which suit his kit, per Ling's own "Core Item Builds" section and four
  independent external sources). This was corrected during development, but
  it highlights that RAG groundedness is only as reliable as the underlying
  corpus — a system can cite its source correctly and still be wrong if the
  source itself is wrong.
- **Hero-tier retrieval nuance**: a question about a specific hero's tier
  (e.g. "What is Gloo's tier?") sometimes surfaces Hero-type chunks instead
  of the dedicated Tier-list chunk, since the hero description is
  semantically closer to the phrasing. Broader "which heroes are SS tier"
  questions correctly surface tier-list data.
- **Windows console encoding**: running generation scripts directly from a
  non-UTF-8 Windows terminal can raise a `UnicodeEncodeError` if the model
  outputs a special character (e.g. an arrow `→`). This does not affect the
  Streamlit interface, which renders over UTF-8/HTTP.
- **Community build data**: an attempt to supplement the knowledge base with
  crowd-submitted builds from an external forum was scoped out due to the
  forum's client-side-only sort/filter UI (no stable URL to scrape) and the
  data being icon-only picks with no explanatory text. A proper version of
  this would need browser automation or a documented API, and is left as
  future work.

## Future Work

- Scrape or license per-hero community build consensus data (see above).
- Expand hero-tier disambiguation (route hero+tier queries to tier-list chunks
  specifically rather than relying purely on embedding similarity).
- Add a dataset/answer-mode selector to the sidebar.
