import pandas as pd

PATH = r"C:\Users\DELL\Desktop\MLBB-RAG\data\mlbb_heroes_cleaned.csv"
df = pd.read_csv(PATH)
print("Columns:", df.columns.tolist())
print("Duplicated columns:", df.columns[df.columns.duplicated()].tolist())
print("Shape:", df.shape)
