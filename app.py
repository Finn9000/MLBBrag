import re
from pathlib import Path

import pandas as pd
import streamlit as st

from rag.generator import generate_answer
from rag.retriever import MLBBRetriever

PROJECT_DIR = Path(__file__).resolve().parent
HEROES_PATH = PROJECT_DIR / "data" / "mlbb_heroes_cleaned.csv"


st.set_page_config(
    page_title="MLBB Guide RAG",
    page_icon="🎮",
    layout="wide",
)


@st.cache_resource
def get_retriever():
    """Load the embedding model and FAISS index only once."""
    return MLBBRetriever()


@st.cache_data
def load_heroes():
    """Load the full hero table (not the chunked version) for hero cards."""
    return pd.read_csv(HEROES_PATH)


def find_mentioned_hero(question, heroes_df):
    """Return the hero row if the question mentions a hero by name, else None."""
    question_lower = question.lower()
    hero_names = sorted(heroes_df["hero_name"].tolist(), key=len, reverse=True)
    for name in hero_names:
        if name.lower() in question_lower:
            return heroes_df[heroes_df["hero_name"] == name].iloc[0]
    return None


def extract_section(document_text, section_keyword):
    """Pull one guide section (e.g. 'Complete Skill Breakdown') out of the
    concatenated document text, which separates sections with 'Open full guide'."""
    sections = document_text.split("Open full guide")
    for section in sections:
        if section_keyword.lower() in section[:80].lower():
            return section.strip()
    return None


def render_hero_card(hero_row):
    """Show a hero image + quick-reference skill panel above the generated answer."""
    st.subheader(f"{hero_row['hero_name']}")
    col_image, col_info = st.columns([1, 2])

    with col_image:
        image_url = hero_row.get("image_url")
        if isinstance(image_url, str) and image_url.startswith("http"):
            st.image(image_url, caption=hero_row["hero_name"], use_container_width=True)
        else:
            st.info("No image available for this hero.")

    with col_info:
        st.markdown(f"**Role:** {hero_row.get('role', 'N/A')}")
        st.markdown(f"**Tags:** {hero_row.get('tags', 'N/A')}")
        description = hero_row.get("description")
        if isinstance(description, str):
            st.markdown(f"**Overview:** {description[:400]}")

    document_text = str(hero_row.get("document", ""))
    skills_text = extract_section(document_text, "Complete Skill Breakdown")
    passive_text = extract_section(document_text, "Passive Skill Deep Dive")
    ultimate_text = extract_section(document_text, "Ultimate Ability Full Guide")

    if skills_text:
        with st.expander("⚔️ Skill Breakdown", expanded=True):
            st.write(skills_text)
    if passive_text:
        with st.expander("✨ Passive Skill"):
            st.write(passive_text)
    if ultimate_text:
        with st.expander("🌟 Ultimate Ability"):
            st.write(ultimate_text)

    st.divider()


st.title("MLBB RAG Search System")
st.write("Ask questions about Mobile Legends heroes and items.")

top_k = st.sidebar.slider(
    "Number of sources (Top-K)",
    min_value=3,
    max_value=10,
    value=5,
)

question = st.text_input(
    "Ask an MLBB question",
    placeholder="Example: What item gives anti-heal?",
)

if st.button("Search", type="primary"):
    if not question.strip():
        st.warning("Please enter a question first.")
    else:
        retriever = get_retriever()
        heroes_df = load_heroes()

        mentioned_hero = find_mentioned_hero(question, heroes_df)
        if mentioned_hero is not None:
            render_hero_card(mentioned_hero)

        with st.spinner("Searching the MLBB knowledge base..."):
            results = retriever.search(question, top_k=top_k)

        with st.spinner("Generating an answer..."):
            try:
                answer = generate_answer(question, results)
                st.subheader("Answer")
                st.write(answer)
            except Exception as error:
                st.error(f"Could not generate an answer: {error}")

        st.subheader("Retrieved Sources")

        for number, result in enumerate(results, start=1):
            with st.expander(
                f"{number}. {result['document_type']}: "
                f"{result['title']} — Similarity: {result['similarity']:.3f}"
            ):
                st.write(result["chunk_text"])
