import duckdb
import pandas as pd 

df = pd.read_csv("regional-global-weekly-2025-03-27.csv")

con = duckdb.connect("spotify_charts.db")
con.execute("CREATE TABLE IF NOT EXISTS charts AS SELECT * FROM df")
con.close()

import streamlit as st
import pandas as pd
import duckdb

con = duckdb.connect("spotify_charts.db")
df = con.execute("SELECT * FROM charts ORDER BY rank").fetchdf()
con.close()

st.title("Spotify Charts Dashboard")
st.dataframe(df)

# Add filters to the sidebar
artist_filter = st.sidebar.selectbox('Select Artist', df['artist_names'].unique())
rank_filter = st.sidebar.slider('Select Rank Range', min_value=1, max_value=200, value=(1, 50))

# Filter the data based on user selection
filtered_data = df[(df['artist_names'] == artist_filter) & 
                   (df['rank'] >= rank_filter[0]) & 
                   (df['rank'] <= rank_filter[1])]

st.write(filtered_data)


# Rank vs Streams plot
import matplotlib.pyplot as plt
import seaborn as sns

# Create the plot figure
fig, ax = plt.subplots(figsize=(8, 6))

# Rank vs Streams plot
st.subheader('Rank vs Streams')
sns.scatterplot(data=df, x='rank', y='streams', ax=ax)
ax.set_title('Rank vs Streams')

# Display the plot using Streamlit
st.pyplot(fig)

# Display a bar chart of top 10 tracks by streams
top_tracks = df.sort_values(by='streams', ascending=False).head(10)
st.subheader('Top 10 Tracks by Streams')
st.bar_chart(top_tracks.set_index('track_name')['streams'])


from wordcloud import WordCloud

# Generate a word cloud of artist names
artist_names = ' '.join(df['artist_names'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(artist_names)

# Display the word cloud
st.subheader('Word Cloud of Artist Names')
st.image(wordcloud.to_array())

from textblob import TextBlob

# Function to get sentiment polarity
def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

# Create a new column for sentiment polarity
df['sentiment'] = df['track_name'].apply(get_sentiment)

# Visualize sentiment distribution
st.subheader('Sentiment Distribution of Track Names')
st.bar_chart(df['sentiment'])



#from textblob import TextBlob
#import matplotlib.pyplot as plt

# Function to get sentiment polarity
def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

# Apply sentiment analysis to the track names
df['sentiment'] = df['track_name'].apply(get_sentiment)

# Plot the sentiment distribution
st.subheader('Sentiment Distribution of Track Names')
plt.figure(figsize=(10, 6))
plt.hist(df['sentiment'], bins=20, edgecolor='black', alpha=0.7)
plt.title('Sentiment Distribution (Polarity) of Track Names')
plt.xlabel('Polarity')
plt.ylabel('Frequency')
st.pyplot()


# for index, row in df.iterrows():
#     with st.expander(f"Details of {row['track_name']}"):
#         st.write(f"Artist: {row['artist_names']}")
#         st.write(f"Rank: {row['rank']}")
#         st.write(f"Streams: {row['streams']}")
#         st.write(f"Peak Rank: {row['peak_rank']}")
#         st.write(f"Weeks on Chart: {row['weeks_on_chart']}")


st.subheader("Summary")
st.write(f"Total Number of Tracks: {df['track_name'].nunique()}")
st.write(f"Total Number of Artists: {df['artist_names'].nunique()}")
st.write(f"Total Streams: {df['streams'].sum()}")
st.write(f"Average Weeks on Chart: {df['weeks_on_chart'].mean():.2f}")


import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Authenticate with Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='c1ab81c749e64523abf3af0dc29b76d9',
                                               client_secret='2380f26f58f44641befc865d62bb5ee1',
                                               redirect_uri='http://localhost:8889/callback',
                                               scope='user-library-read'))

# Get track preview URL
track_uri = df.loc[150, 'uri']  # Example: get the URI of the first track
track_info = sp.track(track_uri)
preview_url = track_info['preview_url']

# Display the preview link
st.subheader(f"Preview of {df.loc[150, 'track_name']}")
st.audio(preview_url)


track = sp.track('6AI3ezQ4o3HUoP6Dhudph3')

# Check if preview_url is available
preview_url = track['preview_url']

if preview_url:
    st.audio(preview_url, format='audio/mp3')  # Display the audio player
else:
    st.write("No preview available for this track.")



import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st

# # Set up Spotify credentials
# CLIENT_ID = 'your-client-id'
# CLIENT_SECRET = 'your-client-secret'
# REDIRECT_URI = 'http://localhost:8899/callback'

# Authenticate using SpotifyOAuth
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
#     client_id=CLIENT_ID,
#     client_secret=CLIENT_SECRET,
#     redirect_uri=REDIRECT_URI,
#     scope="user-library-read"
# ))

# Fetch a track (replace 'track_id' with the actual track ID)
track_id = '21B4gaTWnTkuSh77iWEXdS'
track = sp.track(track_id)

# Get the preview URL
preview_url = track['preview_url']

# Display the audio player if preview is available
if preview_url:
    st.audio(preview_url, format='audio/mp3')
else:
    st.write("No preview available for this track22222.")
