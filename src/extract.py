import pandas as pd 

def extract_movies(filepath):
    movies = pd.read_csv(
        filepath,
        sep="|",
        encoding="latin-1",
        names=[
            "movie_id", "title", "release_date", "video_release_date", "imdb_url",
            "unknown", "Action", "Adventure", "Animation", "Children", "Comedy",
            "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror",
            "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"
        ]
    )
    
    genre_columns = [ 
        "unknown", "Action", "Adventure", "Animation", "Children", "Comedy",
        "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror",
        "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"
    ]

    movies = movies[["movie_id", "title"] + genre_columns]
    return movies    

def extract_ratings(filepath):
    ratings = pd.read_csv(
        filepath,
        sep="\t",
        names=["user_id", "movie_id", "rating", "timestamp"]
    )
    return ratings