import pandas as pd
heroes = pd.read_csv(r"C:\Users\DELL\Desktop\MLBB-RAG\data\mlbb_heroes_cleaned.csv")
ling = heroes[heroes["hero_name"].str.contains("Ling", case=False, na=False)]
print(ling[["hero_name"]])
for doc in ling["document"]:
    print("=" * 60)
    print(doc)
