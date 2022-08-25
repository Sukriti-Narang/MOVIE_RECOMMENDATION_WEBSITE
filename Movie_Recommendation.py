import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel
from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
import time
from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask, send_from_directory
# app = Flask(__name__)

column_names = ["item_id", "movie_title", "release date", "video release date", "IMDb URL", "unknown", "Action", "Adventure", "Animation", "Children's", "Comedy", "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"]
item = pd.read_csv("u.item", sep='|', names = column_names, encoding='latin-1')

movies_list = list(item['movie_title'])

# Keep track of movie title corresponding to the index of dataframe
index_movie_dict = {}
for i in range(len(item)):
    index_movie_dict[i] = item.loc[i]['movie_title']

# Keep track of index of dataframe corresponding to the movie title
movie_index_dict = {}
for i in range(len(item)):
    movie_index_dict[item.loc[i]['movie_title']] = i

# Keep track of release date corresponding to movie title
release_date = item['release date']
movie_release_date_dict = {}
for i in range(len(item)):
    movie_release_date_dict[movies_list[i]] = release_date[i]

item.drop(["item_id", "movie_title", "release date", "video release date", "IMDb URL"], axis = 1, inplace = True)
genres = item.to_numpy()

from sklearn.metrics.pairwise import sigmoid_kernel
genres_similarity_matrix = sigmoid_kernel(genres, genres)

item = pd.read_csv("u.item", sep='|', names = column_names, encoding='latin-1')
posters = pd.read_csv('movie_poster.csv', names = ['item_id', 'poster_link'])
df = posters.merge(item, on="item_id")
df = df.drop(columns=["unknown", "Action", "Adventure", "Animation", "Children's", "Comedy", "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"])

movies_list1 = df['movie_title']
poster_link = df['poster_link']
movie_poster_dict = {}
for i in range(len(df)):
    movie_poster_dict[movies_list1[i]] = poster_link[i]

def recommend():
    img = open('movies.jpg', 'rb').read()
    put_image(img, width='900px')
    put_markdown('# **Movie Recommendation System For `You`**')
    put_html('<h1 style="font-size:20px; text-align:center; color:blue; background-color:powderblue;">Welcome to Hollywood!<br></h1>')
    
    recently_watched_movie = select('Enter one of the movies from the database ', movies_list)
    number_of_recommendations = input("Enter the number of recommendations", type = NUMBER)

    put_markdown('## Please wait! Your request is being processed!')
    
    #Display Processbar
    put_processbar('bar');
    for i in range(1, 11):
        set_processbar('bar', i / 10)
        time.sleep(0.1)

    put_html('<hr>')
    put_markdown("Recommendations for you similar to `%s` movie are as follows: " % recently_watched_movie)
    put_html('<hr>')
    
    idx = movie_index_dict[recently_watched_movie]
    similarity_list = genres_similarity_matrix[idx]
    
    # List of tuples (Similarity value, Index)
    lst = []
    for i in range(len(similarity_list)):
        lst.append((similarity_list[i],i))
    count = 0
    for element in list(sorted(lst, reverse = True)):
        count = count + 1
        if(count == (number_of_recommendations+1)):
            break
        movie_name = index_movie_dict[element[1]]
        put_markdown("# *`%s`*" % movie_name)
        put_text("Release Date: %s" % movie_release_date_dict[movie_name])
        # Display movie poster
        if(movie_name in movie_poster_dict.keys()):
            p_link = movie_poster_dict[movie_name]
            put_image(p_link, width = '1000px')
        else:
            put_text("Oops! Enough information not available.")
        put_html('<hr>')

start_server(recommend, port=8080, debug=True)
# app.add_url_rule('/movierec', 'webio_view', webio_view(recommend), methods=['GET', 'POST', 'OPTIONS'])
# app.run(host='localhost', port=80)
# #app.run()