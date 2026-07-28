import pandas as pd

PATH = r"C:\Users\DELL\Desktop\MLBB-RAG\data\mlbb_heroes_cleaned.csv"
df = pd.read_csv(PATH)

BAD_JUNGLE = (
    "For jungle items, Starlium Scythe suits snowballing scenarios and squishy "
    "enemy compositions, while Corrosion Scythe becomes essential against multiple "
    "tanky heroes or when your team lacks consistent physical damage."
)
GOOD_JUNGLE = (
    "For jungle sustain, Haas's Claws suits standard clears and dueling, while "
    "Corrosion Scythe becomes useful against multiple tanky heroes or when your "
    "team lacks consistent physical damage; avoid Starlium Scythe, which does not "
    "suit Ling's crit-reset playstyle."
)

BAD_PEN = (
    "Penetration choices split between Malefic Roar for percentage armor shred "
    "against tanks like Hylos, Khufra, and Belerick, and Divine Glaive for magic "
    "penetration in hybrid builds."
)
GOOD_PEN = (
    "Malefic Roar is the standard penetration pick for percentage armor shred "
    "against tanks like Hylos, Khufra, and Belerick; avoid Divine Glaive, since "
    "Ling deals purely physical damage and gains no value from magic penetration."
)

mask = df["hero_name"] == "Ling"
count_before = df.loc[mask].apply(
    lambda row: sum(str(v).count(BAD_JUNGLE) + str(v).count(BAD_PEN) for v in row), axis=1
).sum()

for col in df.columns:
    if pd.api.types.is_string_dtype(df[col]) or df[col].dtype == object:
        df.loc[mask, col] = df.loc[mask, col].astype(str).str.replace(
            BAD_JUNGLE, GOOD_JUNGLE, regex=False
        ).str.replace(
            BAD_PEN, GOOD_PEN, regex=False
        )

count_after = df.loc[mask].apply(
    lambda row: sum(str(v).count(BAD_JUNGLE) + str(v).count(BAD_PEN) for v in row), axis=1
).sum()

print(f"Occurrences of bad text before: {count_before}, after: {count_after}")

df.to_csv(PATH, index=False)
print("Saved.")
