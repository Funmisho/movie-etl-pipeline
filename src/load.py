from sqlalchemy import create_engine

def get_db_engine(user, password, host, port, database):
    connection_uri = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(connection_uri)
    return engine

def load_recommendations(recommendations, user_id, engine):
    recommendations["user_id"] = user_id
    recommendations = recommendations[["user_id", "movie_id", "title", "avg_rating"]]
    recommendations.to_sql("recommendations", engine, if_exists="append", index=False)
    print(f"Loaded recommendations for user {user_id}")