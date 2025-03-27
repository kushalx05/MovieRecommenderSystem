import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=74f71dcee8aa01725cec028167277995&language=en-US"
    response = requests.get(url)
    data = response.json()

    # Check if 'poster_path' exists
    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/500"  # Default placeholder image

# Function to recommend movies
def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_movies_posters = []

        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_movies_posters.append(fetch_poster(movie_id))

        return recommended_movies, recommended_movies_posters
    except IndexError:
        st.error("❌ Movie not found in dataset. Please try another movie.")
        return [], []

# Load movie data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title("🎬 Movie Recommender System")
st.markdown("#### Get movie recommendations based on your favorite movies! 🍿")

# User input
selected_movie_name = st.selectbox("🎥 Choose a movie:", movies['title'].values)

# Recommendation button with a spinner
if st.button("🔮 Recommend"):
    with st.spinner("Fetching recommendations..."):
        names, posters = recommend(selected_movie_name)

    # Display recommendations
    if names:
        cols = st.columns(5)
        for i, col in enumerate(cols):
            if i < len(names):
                with col:
                    st.markdown(f"**{names[i]}**")
                    st.image(posters[i], width=150)
