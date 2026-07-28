import ast
import pandas as pd
import sys, os
sys.path.insert(0, r"C:\Users\DELL\Desktop\MLBB-RAG")

# Syntax check
with open(r"C:\Users\DELL\Desktop\MLBB-RAG\app.py", encoding="utf-8") as f:
    ast.parse(f.read())
print("Syntax OK")

# Logic check (without Streamlit)
heroes_df = pd.read_csv(r"C:\Users\DELL\Desktop\MLBB-RAG\data\mlbb_heroes_cleaned.csv")

def find_mentioned_hero(question, heroes_df):
    question_lower = question.lower()
    hero_names = sorted(heroes_df["hero_name"].tolist(), key=len, reverse=True)
    for name in hero_names:
        if name.lower() in question_lower:
            return heroes_df[heroes_df["hero_name"] == name].iloc[0]
    return None

def extract_section(document_text, section_keyword):
    sections = document_text.split("Open full guide")
    for section in sections:
        if section_keyword.lower() in section[:80].lower():
            return section.strip()
    return None

for q in ["Tell me about Ling's skills", "Best build for Fanny", "Who is Yi Sun-shin countered by?", "random question about anti-heal"]:
    hero = find_mentioned_hero(q, heroes_df)
    print(q, "->", hero["hero_name"] if hero is not None else None)

ling_row = heroes_df[heroes_df["hero_name"] == "Ling"].iloc[0]
skills = extract_section(str(ling_row["document"]), "Complete Skill Breakdown")
print("\nSkills section found:", skills is not None)
print(skills[:300] if skills else "NONE")
print("\nImage URL:", ling_row["image_url"])
