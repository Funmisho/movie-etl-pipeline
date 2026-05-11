# Movie Recommendation ETL Pipeline

An end-to-end ETL pipeline that extracts raw movie rating data, transforms it into personalised recommendations, and loads the results into a PostgreSQL database.

Built as a practical introduction to ETL concepts after completing the Introduction to Data Engineering course on DataCamp.

---

## What It Does

For any given user, the pipeline:
1. Identifies their preferred genre based on their rating history
2. Filters out movies they have already seen
3. Excludes movies with fewer than 50 ratings to ensure statistical reliability
4. Ranks remaining eligible movies by average rating
5. Returns the top 3 recommendations and stores them in a database

---

## Pipeline Architecture

```
Raw Data (CSV)
      ↓
Extract (pandas)
      ↓
Transform (genre preference → filter → rank)
      ↓
Load (PostgreSQL)
```

---

## Dataset

[MovieLens 100K](https://grouplens.org/datasets/movielens/100k/) — 100,000 ratings from 943 users across 1,682 movies.

Files used:
- `u.data` — user ratings (user_id, movie_id, rating, timestamp)
- `u.item` — movie metadata (movie_id, title, genres)

---

## Tools

| Tool | Purpose |
|---|---|
| Python | core language |
| pandas | data extraction and transformation |
| SQLAlchemy | database connection layer |
| psycopg2 | PostgreSQL driver |
| PostgreSQL | storage for final recommendations |

---

## Project Structure

```
movie-etl-pipeline/
├── data/
│   ├── u.data
│   └── u.item
├── src/
│   ├── extract.py      # reads raw files into DataFrames
│   ├── transform.py    # recommendation logic
│   ├── load.py         # writes to PostgreSQL
│   └── main.py         # runs the full pipeline
├── notebooks/          # exploratory work
└── README.md
```

---

## How to Run

**1. Clone the repo and set up a virtual environment**
```bash
git clone https://github.com/Funmisho/movie-etl-pipeline.git
cd movie-etl-pipeline
python -m venv venv
source venv/bin/activate
pip install pandas sqlalchemy psycopg2-binary
```

**2. Download the dataset**

Download MovieLens 100K from https://grouplens.org/datasets/movielens/100k/ and place `u.data` and `u.item` in the `data/` folder.

**3. Set up PostgreSQL**

Create a database called `movie_pipeline` and update the `DB_CONFIG` in `main.py` with your credentials.

**4. Run the pipeline**
```bash
cd src
python main.py
```

---

<img width="1010" height="292" alt="image" src="https://github.com/user-attachments/assets/877aecd5-ac57-4e12-9b34-f0cff69edf0d" />


## Sample Output

<img width="939" height="559" alt="image" src="https://github.com/user-attachments/assets/06eeb2bb-70aa-4382-b1e0-ab89773e9d94" />

---

## Key Engineering Concepts Demonstrated

- ETL pipeline design
- Data extraction from heterogeneous raw files (pipe-separated, tab-separated, mixed encodings)
- Data cleaning and transformation with pandas
- Recommendation generation logic (genre inference, eligibility filtering, rating threshold)
- PostgreSQL integration with SQLAlchemy
- Cross-environment networking (WSL2 ↔ Windows PostgreSQL)
- Idempotent database loading (delete before insert to prevent duplicates)
- Modular pipeline architecture (extract / transform / load / main)

---

## Infrastructure Note

This pipeline was developed with the ETL code running on **WSL2 (Linux)** while PostgreSQL was hosted on **Windows**. Connecting across that boundary required:
- Identifying the Windows host IP from WSL (`cat /etc/resolv.conf`)
- Opening an inbound firewall rule for port 5432 on Windows
- Updating `postgresql.conf` to set `listen_addresses = '*'`
- Updating `pg_hba.conf` to trust connections from the WSL subnet

This is a known friction point in local development and worth being aware of in similar setups.

---

## Limitations

- **Simple average rating** — a movie rated 5.0 by 3 people ranks above one rated 4.5 by 500 people. The 50-rating minimum threshold partially addresses this but it is not a complete solution.
- **Rule-based genre preference** — the pipeline picks the single most-watched genre. A user with mixed tastes across multiple genres will get a narrower recommendation than they deserve.
- **No personalisation beyond genre** — two users who both prefer Drama get recommendations from the same pool, differing only in what they have already seen.
- **Static data** — the pipeline runs on a fixed CSV snapshot, not a live data source.

---

## Future Improvements

- Collaborative filtering (recommend based on what similar users liked)
- Weighted rating formula (e.g. Bayesian average) to handle low-sample movies properly
- Multi-genre preference (recommend across top 2 genres instead of just 1)
- Airflow DAG to schedule daily pipeline runs
- Live database source instead of CSV files
