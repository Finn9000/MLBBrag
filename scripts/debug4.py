import pandas as pd

PATH = r"C:\Users\DELL\Desktop\MLBB-RAG\data\mlbb_heroes_cleaned.csv"
df = pd.read_csv(PATH)

BAD_JUNGLE = (
    "For jungle items, Starlium Scythe suits snowballing scenarios and squishy "
    "enemy compositions, while Corrosion Scythe becomes essential against multiple "
    "tanky heroes or when your team lacks consistent physical damage."
)
GOOD_JUNGLE = "TEST_MARKER_JUNGLE"
BAD_PEN = (
    "Penetration choices split between Malefic Roar for percentage armor shred "
    "against tanks like Hylos, Khufra, and Belerick, and Divine Glaive for magic "
    "penetration in hybrid builds."
)
GOOD_PEN = "TEST_MARKER_PEN"

mask = df["hero_name"] == "Ling"

for col in df.columns:
    if df[col].dtype == object:
        df.loc[mask, col] = df.loc[mask, col].astype(str).str.replace(
            BAD_JUNGLE, GOOD_JUNGLE, regex=False
        ).str.replace(
            BAD_PEN, GOOD_PEN, regex=False
        )

check = df.loc[mask, "situational_items"].iloc[0]
print("Marker present in situational_items after loop:", GOOD_JUNGLE in check)
print("Bad text present in situational_items after loop:", BAD_JUNGLE in check)
