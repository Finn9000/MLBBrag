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

s = df.loc[mask, "situational_items"].astype(str)
s2 = s.str.replace(BAD_JUNGLE, GOOD_JUNGLE, regex=False)
print("after first replace, marker present:", GOOD_JUNGLE in s2.iloc[0])
s3 = s2.str.replace(BAD_PEN, GOOD_PEN, regex=False)
print("after second replace, marker1 present:", GOOD_JUNGLE in s3.iloc[0])
print("after second replace, marker2 present:", GOOD_PEN in s3.iloc[0])

df.loc[mask, "situational_items"] = s3
print("after assignment, marker1:", GOOD_JUNGLE in df.loc[mask, "situational_items"].iloc[0])
