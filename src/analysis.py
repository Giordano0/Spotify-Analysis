import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("../data/dataset.csv")

print(df.shape)
print(df.dtypes)
df.head()

# Valori nulli per colonna
print(df.isnull().sum())
print()

# Righe duplicate
print(f"Duplicate rows: {df.duplicated().sum()}")

# Rimuovi duplicati e righe con valori nulli
df = df.drop_duplicates()
df = df.dropna()

# Rimuovi la colonna "Unnamed: 0" che è solo un indice inutile
df = df.drop(columns=["Unnamed: 0"])

print(f"\nDataset after cleaning: {df.shape}")

top_songs = df[["track_name", "artists", "popularity"]]\
    .sort_values("popularity", ascending=False)\
    .drop_duplicates("track_name")\
    .head(10)

print(top_songs.to_string(index=False))

top_artists = df["artists"].value_counts().head(10)

plt.figure(figsize=(10, 5))
sns.barplot(x=top_artists.values, y=top_artists.index, palette="viridis")
plt.title("Top 10 artists by number of tracks")
plt.xlabel("Number of tracks")
plt.ylabel("Artist")
plt.tight_layout()
plt.savefig("../output/charts/top_artists.png", dpi=150, bbox_inches="tight")

plt.figure(figsize=(10, 5))
sns.histplot(df["popularity"], bins=50, color="#534AB7")
plt.title("Popularity distribution")
plt.xlabel("Popularity")
plt.ylabel("Number of songs")
plt.tight_layout()
plt.savefig("../output/charts/popularity_distribution.png", dpi=150, bbox_inches="tight")

top_genres = df.groupby("track_genre")["popularity"]\
    .mean()\
    .sort_values(ascending=False)\
    .head(15)

plt.figure(figsize=(10, 6))
sns.barplot(x=top_genres.values, y=top_genres.index, color="#534AB7")
plt.title("Top 15 genres by average popularity")
plt.xlabel("Average popularity")
plt.ylabel("Genre")
plt.tight_layout()
plt.savefig("../output/charts/top_genres.png", dpi=150, bbox_inches="tight")

plt.figure(figsize=(8, 6))
sns.scatterplot(data=df.sample(3000), x="energy", y="danceability",
                hue="popularity", palette="viridis", alpha=0.6)
plt.title("Energy vs Danceability")
plt.tight_layout()
plt.savefig("../output/charts/energy_danceability.png", dpi=150, bbox_inches="tight")

df["duration_min"] = df["duration_ms"] / 60000

top_duration = df.groupby("track_genre")["duration_min"]\
    .mean()\
    .sort_values(ascending=False)\
    .head(10)

plt.figure(figsize=(10, 5))
sns.barplot(x=top_duration.values, y=top_duration.index, color="#4facfe")
plt.title("Top 10 genres by average duration (min)")
plt.xlabel("Average duration (min)")
plt.ylabel("Genre")
plt.tight_layout()
plt.savefig("../output/charts/duration_by_genre.png", dpi=150, bbox_inches="tight")

cols = ["popularity", "danceability", "energy", "loudness",
        "speechiness", "acousticness", "tempo", "valence"]

plt.figure(figsize=(10, 8))
sns.heatmap(df[cols].corr(), annot=True, fmt=".2f",
            cmap="coolwarm", center=0)
plt.title("Correlation between audio features")
plt.tight_layout()
plt.savefig("../output/charts/correlation_heatmap.png", dpi=150, bbox_inches="tight")

genres = ["pop", "hip-hop", "rock"]
cols = ["danceability", "energy", "acousticness", "valence", "speechiness"]

profile = df[df["track_genre"].isin(genres)]\
    .groupby("track_genre")[cols].mean()

profile.T.plot(kind="bar", figsize=(12, 6), colormap="viridis")
plt.title("Average Audio Profile: Pop vs Hip-Hop vs Rock")
plt.xlabel("Feature")
plt.ylabel("Average Value")
plt.xticks(rotation=45)
plt.legend(title="Genre")
plt.tight_layout()
plt.savefig("../output/charts/genre_profile.png", dpi=150, bbox_inches="tight")