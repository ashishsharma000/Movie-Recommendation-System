import streamlit as st
import pickle
import pandas as pd
import requests
import time

import requests


def fetch_poster(movie_id):
    api_key = "ba4b4fcddc9845c03c13f22b14434cb6"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    try:
        data = requests.get(url).json()

        if data.get('poster_path') is None:
            return "https://via.placeholder.com/500x750?text=No+Image"

        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except:
        return "https://via.placeholder.com/500x750?text=No+Image"


# Load data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))


# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        #fetch poster from api
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
        
    return recommended_movies, recommended_posters


# UI
st.title('🎬 Movie Recommendation System')

selected_movie = st.selectbox(
    "Select a movie",
    movies['title'].values
)

# Button
if st.button('Recommend'):
    names, posters = recommend(selected_movie)

    # 👇 PUT COLUMNS CODE HERE
    col1, col2, col3, col4, col5 = st.columns(5)


    col1.text(names[0])
    col1.image(posters[0])

    col2.text(names[1])
    col2.image(posters[1])

    col3.text(names[2])
    col3.image(posters[2])

    col4.text(names[3])
    col4.image(posters[3])

    col5.text(names[4])
    col5.image(posters[4])
