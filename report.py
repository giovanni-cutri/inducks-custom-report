import pandas as pd
import seaborn as sns

df = pd.read_json("collection.json")

df = df.dropna()

top_appearances = df.loc[df.appearances.str.len() != 0, "appearances"].value_counts()[:10]

df["individual_appearances"] = ["; ".join(map(str, l)) for l in df["appearances"]]
top_individual_appearances = df.loc[df["individual_appearances"] != "", "individual_appearances"].str.split("; ").explode().value_counts()[:10]

top_writers = df.loc[df.writing.str.len() != 0, "writing"].value_counts()[:10]

top_artists = df.loc[df.art.str.len() != 0, "art"].value_counts()[:10]

df["individual_writers"] = ["; ".join(map(str, l)) for l in df["writing"]]
df["individual_artists"] = ["; ".join(map(str, l)) for l in df["art"]]
top_writers = df.loc[df.writing.str.len() != 0, "individual_writers"].value_counts()[:10]
sns.barplot(x = top_writers.values, y = top_writers.index, orient = "h").set(title = "Top ten developers distribution")
sns_plot.figure.savefig("output.png")
