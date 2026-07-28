import pandas as pd

PATH = r"C:\Users\DELL\Desktop\MLBB-RAG\data\mlbb_heroes_cleaned.csv"
df = pd.read_csv(PATH)

BAD_JUNGLE = (
    "For jungle items, Starlium Scythe suits snowballing scenarios and squishy "
    "enemy compositions, while Corrosion Scythe becomes essential against multiple "
    "tanky heroes or when your team lacks consistent physical damage."
)
GOOD_JUNGLE = "TEST_MARKER_JUNGLE"

mask = df["hero_name"] == "Ling"

for col in df.columns:
    if df[col].dtype == object:
        before_val = df.loc[mask, col].iloc[0]
        had_bad = BAD_JUNGLE in str(before_val)
        df.loc[mask, col] = df.loc[mask, col].astype(str).str.replace(
            BAD_JUNGLE, GOOD_JUNGLE, regex=False
        )
        after_val = df.loc[mask, col].iloc[0]
        has_marker = GOOD_JUNGLE in str(after_val)
        if had_bad or has_marker:
            print(f"col={col}, had_bad={had_bad}, has_marker_now={has_marker}")

print("FINAL check on situational_items:", GOOD_JUNGLE in str(df.loc[mask, "situational_items"].iloc[0]))
