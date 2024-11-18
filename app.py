import streamlit as st 
import pickle
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommended_movies(movie):
    index=movies[movies["title"]==movie].index[0]
    distence=sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x:x[1])
    
    recommended_movie_names=[]
    recommended_movie_posters=[]
    for i in distence[1:6]:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names,recommended_movie_posters
    

st.title("Movie Recommender System")

movies=pickle.load(open("movie_list.pkl","rb"))
similarity=pickle.load(open("similarity.pkl","rb"))

movies_list=movies["title"].values

selected_movies=st.selectbox(
    "Type or select a movie from the dropdown",
    movies_list  
)

if st.button("Recommend"):
    names,posters=recommended_movies(selected_movies)
    col_list=st.columns(5)
    for i, col in enumerate(col_list):
        with col:
            st.text(names[i])
            st.image(posters[i])
