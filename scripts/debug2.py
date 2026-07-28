import pandas as pd

PATH = r"C:\Users\DELL\Desktop\MLBB-RAG\data\mlbb_heroes_cleaned.csv"
df = pd.read_csv(PATH)
row = df[df["hero_name"] == "Ling"].iloc[0]

BAD_JUNGLE = (
    "For jungle items, Starlium Scythe suits snowballing scenarios and squishy "
    "enemy compositions, while Corrosion Scythe becomes essential against multiple "
    "tanky heroes or when your team lacks consistent physical damage."
)

val = str(row["situational_items"])
print("Direct substring test:", BAD_JUNGLE in val)
print("len match string:", len(BAD_JUNGLE))
idx = val.find("For jungle items")
print("Actual slice:", repr(val[idx: idx + len(BAD_JUNGLE) + 5]))
