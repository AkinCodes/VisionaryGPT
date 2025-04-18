import os
import shutil
from tmdbv3api import TMDb, Movie

# --- TMDb Setup ---
tmdb = TMDb()
tmdb.api_key = "fe1bdc619115b7d8d6a5fd0183334c30"
tmdb.language = "en"
tmdb.debug = True
movie_api = Movie()

# --- Paths ---
poster_dir = '/Users/akin.olusanya/Downloads/poster_downloads'
output_dir = '/Users/akin.olusanya/Desktop/VisionaryGPT/backend/app/data/poster_genres'

# --- Genre Mapping ---
genres_of_interest = {
    28: 'action',
    35: 'comedy',
    18: 'drama',
    27: 'horror',
    10749: 'romance',
}

# --- Create Folders ---
for genre in genres_of_interest.values():
    os.makedirs(os.path.join(output_dir, genre), exist_ok=True)

# --- Classify and Move ---
def classify_and_move_by_id(tmdb_id, filename):
    try:
        movie_data = movie_api.details(tmdb_id)
        genre_ids = [g['id'] for g in movie_data.genres]

        for gid in genre_ids:
            if gid in genres_of_interest:
                genre = genres_of_interest[gid]
                shutil.move(
                    os.path.join(poster_dir, filename),
                    os.path.join(output_dir, genre, filename)
                )
                print(f"✅ Moved '{filename}' → {genre}")
                return

        print(f"⚠️ No matching genre for TMDb ID {tmdb_id} → Skipping.")

    except Exception as e:
        print(f"🚨 Error with TMDb ID {tmdb_id} ({filename}): {e}")

# --- Loop Through Posters ---
for filename in os.listdir(poster_dir):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        try:
            # Extract TMDb ID from filename like "7.7_50539.jpg"
            tmdb_id = int(filename.split("_")[1].split(".")[0])
            classify_and_move_by_id(tmdb_id, filename)
        except Exception as e:
            print(f"❌ Skipping file '{filename}' due to error: {e}")
