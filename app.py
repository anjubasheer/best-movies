import streamlit as st
import pickle
import pandas as pd
import requests

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
        body { background-color: #f4f4f4; }
        .stApp { background-color: white; padding: 20px; border-radius: 10px; }
        .movie-title { font-size: 18px; font-weight: bold; text-align: center; margin-top: 10px; }
        .stButton > button { border-radius: 8px; font-size: 16px; padding: 10px 20px; }
        .stSelectbox > div { border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)


# --- FETCH MOVIE POSTER ---
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        data = requests.get(url).json()
        poster_path = data.get('poster_path', None)
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"  # Fallback image
    except:
        return "https://via.placeholder.com/500x750?text=Error"


# --- RECOMMENDATION FUNCTION ---
def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_posters = []
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_posters.append(fetch_poster(movie_id))
            recommended_movies.append(movies.iloc[i[0]].title)

        return recommended_movies, recommended_posters
    except:
        return [], []


# --- LOAD MOVIE DATA ---
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# --- TITLE ---
st.title("🎬 Movie Recommendation System")

# --- MOVIE SELECTION ---
movie_titles = movies['title'].astype(str).tolist()
selected_movie = st.selectbox("🎥 Choose a Movie", movie_titles)

# --- SHOW RECOMMENDATIONS ---
if st.button('🔍 Show Recommendations'):
    with st.spinner("Fetching recommendations... ⏳"):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    if recommended_movie_names:
        st.subheader("🔥 Top Recommended Movies for You:")
        cols = st.columns(len(recommended_movie_names))

        for idx, col in enumerate(cols):
            with col:
                st.image(recommended_movie_posters[idx], use_container_width=True)  # ✅ Fixed
                st.markdown(f"<p class='movie-title'>{recommended_movie_names[idx]}</p>", unsafe_allow_html=True)


    else:
        st.error("⚠️ No recommendations found. Try another movie.")






# import streamlit as st
# import pickle
# import pandas as pd
# import requests
#
# def fetch_poster(movie_id):
#     url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
#     data = requests.get(url)
#     data = data.json()
#     poster_path = data['poster_path']
#     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
#     return full_path
#
# def recomend(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]
#     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]
#
#     recomended_movies = []
#     recommended_movie_posters = []
#     for i in movies_list:
#         movie_id = i[0]
#         #fetch poster from api
#         movie_id = movies.iloc[i[0]].movie_id
#         recommended_movie_posters.append(fetch_poster(movie_id))
#         recomended_movies.append(movies.iloc[i[0]].title)
#     return recomended_movies, recommended_movie_posters
#
# movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
# movies = pd.DataFrame(movies_dict)
#
# similarity = pickle.load(open('similarity.pkl', 'rb'))
#
# st.title('Movie Recomender System')
#
#
#
#
#
# # Ensure the movie titles are a list of strings
# movie_titles = movies['title'].astype(str).tolist()  # Convert to a list of strings
#
# # Fix selectbox input
# selected_movies = st.selectbox("Choose a movie", movie_titles)
#
# st.write("You selected:", selected_movies )
#
# # if st.button('Recomend'):
# #     recomendations = recomend(selected_movies)
# #     for i in recomendations:
# #         st.write(i)
#
# if st.button('Show Recommendation'):
#     recommended_movie_names,recommended_movie_posters = recomend(selected_movies)
#     col1, col2, col3, col4, col5 = st.columns(5)
#     with col1:
#         # st.text(recommended_movie_names[0])
#         st.image(recommended_movie_posters[0])
#     with col2:
#         # st.text(recommended_movie_names[1])
#         st.image(recommended_movie_posters[1])
#
#     with col3:
#         #st.text(recommended_movie_names[2])
#         st.image(recommended_movie_posters[2])
#     with col4:
#         #st.text(recommended_movie_names[3])
#         st.image(recommended_movie_posters[3])
#     with col5:
#         #st.text(recommended_movie_names[4])
#         st.image(recommended_movie_posters[4])

