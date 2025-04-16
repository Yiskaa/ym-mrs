from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import os

app = Flask(__name__)

movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:6]:  # Get top 5 recommendations
            recommended_movie_names.append(movies.iloc[i[0]].title)
            recommended_movie_posters.append(movies.iloc[i[0]].poster_links)
        
        return recommended_movie_names, recommended_movie_posters
    except IndexError:
        return [], []

@app.route("/")
def index():
    return render_template("index.html", movie_list=movies['title'].values)

@app.route("/recommend", methods=["POST"])
def recommend_movies():
    movie = request.json.get("movie")  # Get movie from JSON
    recommended_names, recommended_posters = recommend(movie)

    return jsonify({
        'recommended_names': recommended_names,
        'recommended_posters': recommended_posters
    })

if __name__ == "__main__":
    app.run(debug=True)
