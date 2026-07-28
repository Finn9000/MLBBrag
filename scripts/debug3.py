import pandas as pd

PATH = r"C:\Users\DELL\Desktop\MLBB-RAG\data\mlbb_heroes_cleaned.csv"
df = pd.read_csv(PATH)

BAD_JUNGLE = (
    "For jungle items, Starlium Scythe suits snowballing scenarios and squishy "
    "enemy compositions, while Corrosion Scythe becomes essential against multiple "
    "tanky heroes or when your team lacks consistent physical damage."
)
GOOD_JUNGLE = "TEST_REPLACEMENT_MARKER"

mask = df["hero_name"] == "Ling"
print("Rows matched:", mask.sum())

before = df.loc[mask, "situational_items"].iloc[0]
print("Contains bad text before:", BAD_JUNGLE in before)

new_series = df.loc[mask, "situational_items"].astype(str).str.replace(BAD_JUNGLE, GOOD_JUNGLE, regex=False)
print("Contains bad text in new_series:", BAD_JUNGLE in new_series.iloc[0])
print("Contains marker in new_series:", GOOD_JUNGLE in new_series.iloc[0])

df.loc[mask, "situational_items"] = new_series
after = df.loc[mask, "situational_items"].iloc[0]
print("Contains bad text after assignment:", BAD_JUNGLE in after)
print("Contains marker after assignment:", GOOD_JUNGLE in after)
