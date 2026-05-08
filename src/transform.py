import pandas as pd

def get_avg_ratings(ratings):
    avg_ratings = ratings.groupby("movie_id")["rating"].mean().reset_index()
    avg_ratings.columns = ["movie_id", "avg_rating"]
    return avg_ratings

def get_user_preferred_genre(user_id, ratings, movies):
    # get all movies this user has rated
    user_ratings = ratings[ratings["user_id"] == user_id]

    # join with movies to get genre info
    user_movies = user_ratings.merge(movies, on="movie_id")

    # genre columns only
    genre_columns = [
        "unknown", "Action", "Adventure", "Animation", "Children", "Comedy",
        "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror",
        "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"
    ]

    # sum each genre column, highest sum is their most watched genre
    genre_totals = user_movies[genre_columns].sum()
    preferred_genre = genre_totals.idxmax()

    return preferred_genre

def get_recommendations(user_id, ratings, movies, avg_ratings, top_n=3):
    # get preferred genre
    preferred_genre = get_user_preferred_genre(user_id, ratings, movies)

    # movies users have already rated
    already_rated = ratings[ratings["user_id"] == user_id]["movie_id"].to_list()

    # rating count filter
    rating_counts = ratings.groupby("movie_id")["rating"].count().reset_index()
    rating_counts.columns = ["movie_id", "rating_count"]
    avg_ratings_filtered = avg_ratings.merge(rating_counts, on="movie_id")
    avg_ratings_filtered = avg_ratings_filtered[avg_ratings_filtered["rating_count"] >= 50]

    # filter movies by preferred genre, exclude already rated
    eligible_movies = movies[
        (movies[preferred_genre] == 1) &
        (~movies["movie_id"].isin(already_rated))
    ]

    # merge with average ratings
    eligible_with_ratings = eligible_movies.merge(avg_ratings_filtered, on="movie_id")

    # sort by avg ratings, take top N
    recommendations = eligible_with_ratings.sort_values(
        "avg_rating", ascending=False
    ).head(top_n)

    return recommendations[["movie_id", "title", "avg_rating"]].reset_index(drop=True)

