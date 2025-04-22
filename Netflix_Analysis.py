#import libaries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#importfile
df = pd.read_csv(r"D:\Python Project\Netflix Project\netflix_titles.csv\netflix_titles.csv")
print(df.head())
#basic information
df.shape
df.columns
df.info()
df.describe
#handelling missing Value
#Drops any row where either title or type is missing (null).
#These two fields are essential for analysis (you can't have a show without a title or type).
df.dropna(subset=['title', 'type'], inplace=True)
#Fills missing values in these columns with 'Not Available' (a placeholder).
#This avoids issues during analysis or visualization by ensuring all rows have values.
df['director'] = df['director'].fillna('Not Available')
df['cast'] = df['cast'].fillna('Not Available')
df['country'] = df['country'].fillna('Not Available')
df['date_added'] = df['date_added'].fillna('Unknown')
df['rating'] = df['rating'].fillna('Unknown')
df['listed_in'] = df['listed_in'].fillna('Not Available')
df['description'] = df['description'].fillna('Not Available')
#insight
#1. Content Type Breakdown
type_counts = df['type'].value_counts()
type_counts.plot(kind='bar', color=['red', 'blue'])
plt.title('Number of Movies vs TV Shows')
plt.xlabel('Type')
plt.ylabel('Count')
plt.show()

#2. Top Contributing Countries
top_countries = df['country'].value_counts().head(10)
top_countries.plot(kind='barh', color='skyblue')
plt.title('Top 10 Countries Producing Netflix Content')
plt.xlabel('Country')
plt.ylabel('Number of Titles')
plt.show()

# Filter Movies and TV Shows data
df_movies = df[df['type'] == 'Movie']
df_tv = df[df['type'] == 'TV Show']

# Create a figure with 2 subplots (side by side)
fig, ax = plt.subplots(1, 2, figsize=(16, 8))

# Plot for Movies Rating Distribution
sns.countplot(x='rating', data=df_movies, palette='Set2', ax=ax[0])
ax[0].set_title('Number of Movies per Rating')
ax[0].set_xlabel('Movie Rating')
ax[0].set_ylabel('Movie Count')
ax[0].tick_params(axis='x', rotation=45)  # Rotate x-axis labels for readability

# Plot for TV Shows Rating Distribution
sns.countplot(x='rating', data=df_tv, palette='Set2', ax=ax[1])
ax[1].set_title('Number of TV Shows per Rating')
ax[1].set_xlabel('TV Show Rating')
ax[1].set_ylabel('TV Show Count')
ax[1].tick_params(axis='x', rotation=45)  # Rotate x-axis labels for readability

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plots
plt.show()

#3. Most Popular Genres/Categories
from collections import Counter
genres = df['listed_in'].dropna().str.split(', ')
flat_genres = [genre for sublist in genres for genre in sublist]
top_genres = pd.Series(Counter(flat_genres)).sort_values(ascending=False).head(10)

top_genres.plot(kind='bar', color='orange')
plt.title('Top 10 Netflix Genres')
plt.xlabel('Genre')
plt.ylabel('Number of Titles')
plt.show()

#4. Country-wise Genre Preferences (Top 5 countries)
top_5_countries = df[df['country']!='Not Available']['country'].value_counts().head(5).index
genre_data = []

for country in top_5_countries:
    genres = df[df['country'] == country]['listed_in'].dropna().str.split(', ')
    flat_genres = [genre for sublist in genres for genre in sublist]
    genre_counts = pd.Series(flat_genres).value_counts().head(5)
    
    for genre, count in genre_counts.items():
        genre_data.append({'Country': country, 'Genre': genre, 'Count': count})
        genre_df = pd.DataFrame(genre_data)
        plt.figure(figsize=(14, 7))
        sns.barplot(data=genre_df, x='Count', y='Genre', hue='Country')
        plt.title('Top 5 Genres in Top 5 Countries on Netflix')
        plt.xlabel('Number of Titles')
        plt.ylabel('Genre')
        plt.legend(title='Country')
        plt.tight_layout()
        plt.show()

#5. Average Duration of Movies
movies_df = df[df['type'] == 'Movie'].copy()
movies_df['duration'] = movies_df['duration'].str.replace(' min', '').astype(float)
avg_duration = movies_df['duration'].mean()
print(f"Average Movie Duration: {avg_duration:.2f} minutes")

#6. Duration Analysis
# Prepare data for movies
df_movies = df[df['type'] == 'Movie'].copy()
df_movies['duration_int'] = df_movies['duration'].str.extract('(\d+)').astype(float)

# Prepare data for TV shows
df_tv = df[df['type'] == 'TV Show'].copy()
df_tv['duration_int'] = df_tv['duration'].str.extract('(\d+)').astype(float)

# Plot side-by-side
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Movie Duration Plot
sns.histplot(df_movies['duration_int'], bins=30, color='green', ax=axes[0])
axes[0].set_title('Movie Duration Distribution')
axes[0].set_xlabel('Duration (minutes)')
axes[0].set_ylabel('Count')

# TV Show Seasons Plot
sns.histplot(df_tv['duration_int'], bins=int(df_tv['duration_int'].max()), color='blue', ax=axes[1])
axes[1].set_title('TV Show Seasons Distribution')
axes[1].set_xlabel('Number of Seasons')
axes[1].set_ylabel('Count')
axes[1].set_xticks(range(1, int(df_tv['duration_int'].max()) + 1))

plt.tight_layout()
plt.show()

#7. Date Added to Netflix
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['year_added'] = df['date_added'].dt.year

sns.countplot(x='year_added', data=df, palette='magma')
plt.title('Number of Titles Added Each Year')
plt.xlabel('Year')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()

#8. Content Growth Over Time
df.groupby('year_added')['show_id'].count().plot(kind='line', marker='o', color='blue')
plt.title('Netflix Content Growth Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Titles')
plt.grid(True)
plt.show()

#9. Top Directors
# Filter out 'Not Available' before getting top 10
top_directors = df[df['director'] != 'Not Available']['director'].value_counts().head(10)
top_directors.plot(kind='barh', color='teal')
plt.title('Top 10 Directors on Netflix')
plt.xlabel('Number of Titles')
plt.ylabel('Director')
plt.show()


#10. Popular Keywords in Netflix's Content Library
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# Combine all descriptions into one large string
text = ' '.join(df['description'].dropna())

# Define stopwords to exclude common words
stopwords = set(STOPWORDS)

# Generate the WordCloud
wordcloud = WordCloud(width=800, height=400, background_color='black', stopwords=stopwords, colormap='viridis').generate(text)

# Display the WordCloud
plt.figure(figsize=(14, 7))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Netflix Content Themes WordCloud', fontsize=20)
plt.show()