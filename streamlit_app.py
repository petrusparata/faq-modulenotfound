import streamlit as st
import random
import sqlite3
import pandas as pd
import plotly.express as px
import datetime
import webbrowser
import urllib.parse

# Initialize SQLite database


def init_db():
    conn = sqlite3.connect("moodvibe.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS mood_history 
                 (timestamp TEXT, mood TEXT)''')
    conn.commit()
    conn.close()

# Save mood to database


def save_mood(mood):
    conn = sqlite3.connect("moodvibe.db")
    c = conn.cursor()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute(
        "INSERT INTO mood_history (timestamp, mood) VALUES (?, ?)", (timestamp, mood))
    conn.commit()
    conn.close()

# Get mood history for trend analysis


def get_mood_history():
    conn = sqlite3.connect("moodvibe.db")
    df = pd.read_sql_query("SELECT timestamp, mood FROM mood_history", conn)
    conn.close()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df


# Sample recommendation data with streaming links
recommendations = {
    "happy": {
        "movies": [
            {"title": "The Lego Movie",
                "netflix_url": "https://www.netflix.com/search?q=The%20Lego%20Movie"},
            {"title": "Up", "netflix_url": "https://www.netflix.com/search?q=Up"},
            {"title": "La La Land",
                "netflix_url": "https://www.netflix.com/search?q=La%20La%20Land"}
        ],
        "music": [
            {"title": "Pharrell Williams - Happy",
                "spotify_url": "https://open.spotify.com/search/Happy%20Pharrell%20Williams"},
            {"title": "ABBA - Dancing Queen",
                "spotify_url": "https://open.spotify.com/search/Dancing%20Queen%20ABBA"},
            {"title": "The Beatles - Here Comes the Sun",
                "spotify_url": "https://open.spotify.com/search/Here%20Comes%20the%20Sun%20The%20Beatles"}
        ],
        "books": [
            {"title": "The Rosie Project",
                "amazon_url": "https://www.amazon.com/s?k=The+Rosie+Project"},
            {"title": "Big Little Lies",
                "amazon_url": "https://www.amazon.com/s?k=Big+Little+Lies"},
            {"title": "Eleanor Oliphant Is Completely Fine",
                "amazon_url": "https://www.amazon.com/s?k=Eleanor+Oliphant+Is+Completely+Fine"}
        ]
    },
    "sad": {
        "movies": [
            {"title": "The Fault in Our Stars",
                "netflix_url": "https://www.netflix.com/search?q=The%20Fault%20in%20Our%20Stars"},
            {"title": "Inside Out",
                "netflix_url": "https://www.netflix.com/search?q=Inside%20Out"},
            {"title": "Moonlight",
                "netflix_url": "https://www.netflix.com/search?q=Moonlight"}
        ],
        "music": [
            {"title": "Adele - Someone Like You",
                "spotify_url": "https://open.spotify.com/search/Someone%20Like%20You%20Adele"},
            {"title": "Billie Eilish - Everything I Wanted",
                "spotify_url": "https://open.spotify.com/search/Everything%20I%20Wanted%20Billie%20Eilish"},
            {"title": "Sam Smith - Stay With Me",
                "spotify_url": "https://open.spotify.com/search/Stay%20With%20Me%20Sam%20Smith"},
            {"title": "Sweater Weather - The Neighbourhood",
                "spotify_url": "https://open.spotify.com/search/The%20Neighbourhood%20Sweater%20Weather"},
            {"title": "XXXTentacion - Numb",
                "spotify_url": "https://open.spotify.com/search/Numb%20XXXTentacion"},
            {"title": "Luke Willies - Everything works out in the end",
                "spotify_url": "https://open.spotify.com/search/ Everything%20works%20out%20in%20the%20end%20Luke%20Willies"},
            {"title": "Lana Del Rey - I wanna Be Yours X Summertime Sadness",
                "spotify_url": "https://open.spotify.com/search/ I%20wanna%20Be%20Yours%20X%20Summertime%20Sadness%20Lana%20Del%20Rey"},
            {"title": "Tom Odell - Another Love",
                "spotify_url": "https://open.spotify.com/search/Tom%20Odell%20X%20Another%20Love"},
            {"title": "inigo quintero - Si No Estas Letra",
                "spotify_url": "https://open.spotify.com/search/Si%20No%20Estas%20Letra%20X%20inigo%20quintero"}
        ],
        "books": [
            {"title": "A Man Called Ove",
                "amazon_url": "https://www.amazon.com/s?k=A+Man+Called+Ove"},
            {"title": "The Book Thief",
                "amazon_url": "https://www.amazon.com/s?k=The+Book+Thief"},
            {"title": "Me Before You",
                "amazon_url": "https://www.amazon.com/s?k=Me+Before+You"}
        ]
    },
    "energetic": {
        "movies": [
            {"title": "Mad Max: Fury Road",
                "netflix_url": "https://www.netflix.com/search?q=Mad+Max%20Fury%20Road"},
            {"title": "The Avengers",
                "netflix_url": "https://www.netflix.com/search?q=The%20Avengers"},
            {"title": "Fast & Furious",
                "netflix_url": "https://www.netflix.com/search?q=Fast%20and%20Furious"}
        ],
        "music": [
            {"title": "Dua Lipa - Don't Start Now",
                "spotify_url": "https://open.spotify.com/search/Don't%20Start%20Now%20Dua%20Lipa"},
            {"title": "The Weeknd - Blinding Lights",
                "spotify_url": "https://open.spotify.com/search/Blinding%20Lights%20The%20Weeknd"},
            {"title": "Skrillex - Bangarang",
                "spotify_url": "https://open.spotify.com/search/Bangarang%20Skrillex"},
            {"title": "Lady Gaga - Bloody Mary",
                "spotify_url": "https://open.spotify.com/search/ Bloody%20Mary%20Lady%20Gaga"},
            {"title": "NCTS - Next!",
                "spotify_url": "https://open.spotify.com/search/ Next!%20NCTS"},
            {"title": "Svlient ft Bernz  - Unlocked Utra Slowed",
                "spotify_url": "https://open.spotify.com/search/ Unlocked%20Utra%20Slowed%20Svlient%20ft%20Bernz"}
        ],
        "books": [
            {"title": "Ready Player One",
                "amazon_url": "https://www.amazon.com/s?k=Ready+Player+One"},
            {"title": "The Martian",
                "amazon_url": "https://www.amazon.com/s?k=The+Martian"},
            {"title": "Project Hail Mary",
                "amazon_url": "https://www.amazon.com/s?k=Project+Hail+Mary"}
        ]
    },
    "relaxed": {
        "movies": [
            {"title": "Amélie", "netflix_url": "https://www.netflix.com/search?q=Amélie"},
            {"title": "The Grand Budapest Hotel",
                "netflix_url": "https://www.netflix.com/search?q=The%20Grand%20Budapest%20Hotel"},
            {"title": "Midnight in Paris",
                "netflix_url": "https://www.netflix.com/search?q=Midnight%20in%20Paris"}
        ],
        "music": [
            {"title": "Norah Jones - Come Away With Me",
                "spotify_url": "https://open.spotify.com/search/Come%20Away%20With%20Me%20Norah%20Jones"},
            {"title": "Jack Johnson - Better Together",
                "spotify_url": "https://open.spotify.com/search/Better%20Together%20Jack%20Johnson"},
            {"title": "Enya - Only Time",
                "spotify_url": "https://open.spotify.com/search/Only%20Time%20Enya"},
            {"title": "Egzod ft Neoni -Maestro Chives Royalty",
                "spotify_url": "https://open.spotify.com/search/Maestro%20Chives%20Royalty%20Egzod%20ft%20Neoni"}
        ],
        "books": [
            {"title": "The Secret Garden",
                "amazon_url": "https://www.amazon.com/s?k=The+Secret+Garden"},
            {"title": "Anne of Green Gables",
                "amazon_url": "https://www.amazon.com/s?k=Anne+of+Green+Gables"},
            {"title": "The Alchemist",
                "amazon_url": "https://www.amazon.com/s?k=The+Alchemist"}
        ]
    }
}

# Initialize database
init_db()

# Streamlit app
st.title("MoodVibe: Media Recommender")
st.write("Select your mood to get personalized media recommendations!")

# Mood selection
mood = st.selectbox("Choose your mood:", [
                    "", "Happy", "Sad", "Energetic", "Relaxed"], index=0)

if mood:
    mood_key = mood.lower()
    if mood_key in recommendations:
        # Save mood to database
        save_mood(mood_key)

        # Randomly select one recommendation per category
        movie = random.choice(recommendations[mood_key]["movies"])
        music = random.choice(recommendations[mood_key]["music"])
        book = random.choice(recommendations[mood_key]["books"])

        # Display recommendations
        st.header(f"Your {mood} Recommendations")

        st.subheader("Movie")
        st.write(movie["title"])
        if st.button("Watch on Netflix", key="movie_stream"):
            webbrowser.open(movie["netflix_url"])

        st.subheader("Music")
        st.write(music["title"])
        if st.button("Listen on Spotify", key="music_stream"):
            webbrowser.open(music["spotify_url"])

        st.subheader("Book")
        st.write(book["title"])
        if st.button("Find on Amazon", key="book_stream"):
            webbrowser.open(book["amazon_url"])

        # Social sharing
        st.subheader("Share Your Recommendations")
        share_text = f"Feeling {mood}? Check out my MoodVibe picks: Movie - {movie['title']}, Music - {music['title']}, Book - {book['title']} #MoodVibe"
        st.write("Copy this text to share:")
        st.code(share_text)
        if st.button("Share on X"):
            encoded_text = urllib.parse.quote(share_text)
            x_url = f"https://x.com/intent/tweet?text={encoded_text}"
            webbrowser.open(x_url)

        # Mood trend analysis
        st.subheader("Mood Trend Analysis")
        df = get_mood_history()
        if not df.empty:
            # Filter last 30 days
            thirty_days_ago = datetime.datetime.now() - datetime.timedelta(days=30)
            df = df[df['timestamp'] >= thirty_days_ago]
            # Count mood occurrences
            mood_counts = df['mood'].value_counts().reset_index()
            mood_counts.columns = ['Mood', 'Count']
            # Plot
            fig = px.line(mood_counts, x='Mood', y='Count',
                          title="Mood Trends (Last 30 Days)", markers=True)
            st.plotly_chart(fig)
        else:
            st.write(
                "No mood history available yet. Keep selecting moods to see trends!")
    else:
        st.error("Please select a valid mood.")
