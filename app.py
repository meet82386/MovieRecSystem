import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    res = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8a16f199efb18a3102ba6d1054a51dfe&language=en-US'.format(movie_id))
    data = res.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommand(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommanded_movies = []
    recommanded_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommanded_movies.append(movies.iloc[i[0]].title)
        # Fetch poster from api
        recommanded_movies_poster.append(fetch_poster(movie_id))
    return recommanded_movies,recommanded_movies_poster
    

movie_dict = pickle.load(open('moviesDict.pkl','rb'))
movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open('similarity.pkl','rb'))


st.title('Movie Recommander System')

Selected_movie = st.selectbox(
    'What is your favourite movie ? ',
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommand(Selected_movie)
    
    this_tup = st.columns(5)
    c = 0
    for i in this_tup:
        with i:
            st.text(names[c])
            st.image(posters[c])
        c += 1
    