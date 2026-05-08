from extract import extract_movies, extract_ratings
from transform import get_avg_ratings, get_recommendations
from load import get_db_engine, load_recommendations

# --- CONFIG ---
MOVIES_PATH = "../data/u.item"
RATINGS_PATH = "../data/u.data"

DB_CONFIG = {
    "user": "postgres",
    "password": "020403",
    "host": "172.18.32.1",
    "port": "5432",
    "database": "movie_pipeline"
}

# --- PIPELINE ---
def run_pipeline(user_ids):
    print("Extracting data...")
    movies = extract_movies(MOVIES_PATH)
    ratings = extract_ratings(RATINGS_PATH)

    print("Transforming data...")
    avg_ratings = get_avg_ratings(ratings)

    print("Loading recommendations...")
    engine = get_db_engine(**DB_CONFIG)

    for user_id in user_ids:
        recs = get_recommendations(user_id, ratings, movies, avg_ratings)
        load_recommendations(recs, user_id, engine)

    print("Pipeline complete.")

if __name__ == "__main__":
     # run for a sample of users
    run_pipeline(user_ids=[1, 2, 3, 4, 5])