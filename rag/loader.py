from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"


def load_knowledge_base():
    heroes = pd.read_csv(DATA_DIR / "mlbb_heroes_cleaned.csv")
    items = pd.read_csv(DATA_DIR / "mlbb_items_cleaned.csv")
    tierlist = pd.read_csv(DATA_DIR / "mlbb_tierlist_mythic_2026-07-27.csv")

    hero_docs = heroes[["hero_name", "document"]].copy()
    hero_docs.columns = ["title", "document"]
    hero_docs["document_type"] = "Hero"

    item_docs = items[["item_name", "document"]].copy()
    item_docs.columns = ["title", "document"]
    item_docs["document_type"] = "Item"

    tierlist_docs = tierlist[["hero_name", "document"]].copy()
    tierlist_docs.columns = ["title", "document"]
    tierlist_docs["document_type"] = "Tierlist"

    knowledge_base = pd.concat(
        [hero_docs, item_docs, tierlist_docs], ignore_index=True
    )
    knowledge_base.insert(0, "document_id", range(1, len(knowledge_base) + 1))

    return knowledge_base


if __name__ == "__main__":
    knowledge_base = load_knowledge_base()

    print(f"Loaded {len(knowledge_base)} documents.")
    print(knowledge_base[["document_id", "document_type", "title"]].head())