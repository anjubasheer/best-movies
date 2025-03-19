import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recomend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]

    recomended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = i[0]
        #fetch poster from api
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recomended_movies.append(movies.iloc[i[0]].title)
    return recomended_movies, recommended_movie_posters

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recomender System')





# Ensure the movie titles are a list of strings
movie_titles = movies['title'].astype(str).tolist()  # Convert to a list of strings

# Fix selectbox input
selected_movies = st.selectbox("Choose a movie", movie_titles)

st.write("You selected:", selected_movies )

# if st.button('Recomend'):
#     recomendations = recomend(selected_movies)
#     for i in recomendations:
#         st.write(i)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recomend(selected_movies)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])




