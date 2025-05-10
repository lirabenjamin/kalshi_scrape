import os, csv, requests, time
from dotenv import load_dotenv
from pprint import pprint
import pandas as pd
from pathlib import Path

load_dotenv()

API = "https://www.metaculus.com/api"
TOKEN = os.getenv("METACULUS_TOKEN")
if not TOKEN:
    raise RuntimeError("Missing METACULUS_TOKEN. Add it to your .env file or environment variables.")
HEAD  = {"Authorization": f"Token {TOKEN}"}

fields = [
    "id", "title", "url",
    "created_time", "scheduled_close_time", "actual_close_time",
    "possibility_type", "project_title", "category_descriptions",
    "comment_count", "forecasts_count", "nr_forecasters",
    "description", "resolution_criteria"
]
rows   = []

cumulative_saved = 0

# --- basic caching: read existing CSV to avoid re‑downloading the same IDs
cache_path = Path("metaculus_open_questions.csv")
cached_ids = set()
if cache_path.exists():
    try:
        cached_df = pd.read_csv(cache_path, usecols=["id"])
        cached_ids = set(cached_df["id"].tolist())
        print(f"Loaded {len(cached_ids)} cached IDs – will skip duplicates.")
    except Exception as e:
        print(f"Cache read failed ({e}); starting fresh.")

SLEEP_SEC = 2.0  # stay well under 1 000 req/hr

url = f"{API}/posts/?type=question&limit=100"
while url:
    resp = requests.get(url, headers=HEAD, timeout=15)
    resp.raise_for_status()
    payload = resp.json()
    data    = payload.get("results", [])

    if not data:
        break

    page_rows = []

    for post in data:
        if post["id"] in cached_ids:
            continue  # already stored
        q         = post.get("question") or {}
        proj      = post.get("projects") or {}
        categories = proj.get("category") or []
        default_proj = proj.get("default_project") or {}

        cat_desc  = "; ".join(c.get("description", "") for c in categories)
        page_rows.append(row := {
            "id":          post["id"],
            "title":       post["title"],
            "url":         f"https://www.metaculus.com/questions/{post['id']}/{post['slug']}/",
            "created_time": post["created_at"],
            "scheduled_close_time": post.get("scheduled_close_time", ""),
            "actual_close_time":    post.get("actual_close_time", ""),
            "possibility_type":     q.get("type", ""),
            "project_title":        default_proj.get("name", ""),
            "category_descriptions": cat_desc,
            "comment_count":   post.get("comment_count", ""),
            "forecasts_count": post.get("forecasts_count", ""),
            "nr_forecasters":  post.get("nr_forecasters", ""),
            "description":          q.get("description", ""),
            "resolution_criteria":  q.get("resolution_criteria", "")
        })
        cached_ids.add(post["id"])   # update cache set immediately

    # ---- write this page immediately
    if page_rows:
        mode = "a" if cache_path.exists() else "w"
        with open(cache_path, mode, newline="") as f:
            wr = csv.DictWriter(f, fieldnames=fields)
            if mode == "w":
                wr.writeheader()
            wr.writerows(page_rows)

    cumulative_saved += len(page_rows)
    url = payload.get("next")
    print(f"[batch] API returned {len(data):>3} posts | "
          f"saved {len(page_rows):>3} new | "
          f"cumulative {cumulative_saved}",
          flush=True)

    if url:
        time.sleep(SLEEP_SEC)          # be polite; limit is 1k req/hr

print(f"Finished. Added {cumulative_saved} new questions to {cache_path}.")