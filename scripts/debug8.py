import pandas as pd

PATH = r"C:\Users\DELL\Desktop\MLBB-RAG\data\mlbb_heroes_cleaned.csv"
df = pd.read_csv(PATH)
mask = df["hero_name"] == "Ling"
print("mask sum:", mask.sum())
print("dtypes:\n", df.dtypes)
val = df.loc[mask, "situational_items"]
print("type of val:", type(val))
print("len:", len(val))
print("first 100 chars:", str(val.iloc[0])[:100])
