import pandas as pd, re

PATH = r"C:\Users\DELL\Desktop\MLBB-RAG\data\mlbb_heroes_cleaned.csv"
df = pd.read_csv(PATH)
row = df[df["hero_name"] == "Ling"].iloc[0]

for col in df.columns:
    val = str(row[col])
    idx = val.find("Starlium Scythe")
    if idx != -1:
        print(f"--- column: {col} ---")
        print(repr(val[max(0, idx-60):idx+200]))
        print()
