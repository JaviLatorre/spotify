"""Generate static The Smiths JSON data files for offline web app."""
import json
import random
import math
from pathlib import Path

random.seed(42)

ALBUMS = [
    {"name": "The Smiths",                 "year": 1984, "release_date": "1984-02-20"},
    {"name": "Meat Is Murder",             "year": 1985, "release_date": "1985-02-11"},
    {"name": "The Queen Is Dead",          "year": 1986, "release_date": "1986-06-16"},
    {"name": "Strangeways, Here We Come",  "year": 1987, "release_date": "1987-09-28"},
]

TRACKS = {
    "The Smiths": [
        "Reel Around the Fountain",
        "You've Got Everything Now",
        "Miserable Lie",
        "Pretty Girls Make Graves",
        "The Hand That Rocks the Cradle",
        "This Charming Man",
        "Still Ill",
        "Hand in Glove",
        "What Difference Does It Make?",
        "I Don't Owe You Anything",
        "Suffer Little Children",
    ],
    "Meat Is Murder": [
        "The Headmaster Ritual",
        "Rusholme Ruffians",
        "I Want the One I Can't Have",
        "What She Said",
        "That Joke Isn't Funny Anymore",
        "Nowhere Fast",
        "Well I Wonder",
        "Barbarism Begins at Home",
        "Meat Is Murder",
    ],
    "The Queen Is Dead": [
        "The Queen Is Dead",
        "Frankly, Mr. Shankly",
        "I Know It's Over",
        "Never Had No One Ever",
        "Cemetery Gates",
        "Bigmouth Strikes Again",
        "The Boy with the Thorn in His Side",
        "Vicar in a Tutu",
        "There Is a Light That Never Goes Out",
        "Some Girls Are Bigger Than Others",
    ],
    "Strangeways, Here We Come": [
        "A Rush and a Push and the Land Is Ours",
        "I Started Something I Couldn't Finish",
        "Death of a Disco Dancer",
        "Girlfriend in a Coma",
        "Stop Me If You Think You've Heard This One Before",
        "Last Night I Dreamt That Somebody Loved Me",
        "Unhappy Birthday",
        "Paint a Vulgar Picture",
        "Death at One's Elbow",
        "I Won't Share You",
    ],
}

# Per-album audio feature profiles (mean, std) — based on musical character of each album
PROFILES = {
    "The Smiths": {
        "energy":           (0.65, 0.12),
        "danceability":     (0.50, 0.10),
        "valence":          (0.40, 0.14),
        "acousticness":     (0.15, 0.09),
        "instrumentalness": (0.02, 0.03),
        "liveness":         (0.12, 0.06),
        "speechiness":      (0.08, 0.03),
        "loudness":         (-8.2, 1.8),
        "tempo":            (140,  18),
    },
    "Meat Is Murder": {
        "energy":           (0.60, 0.14),
        "danceability":     (0.48, 0.10),
        "valence":          (0.30, 0.12),
        "acousticness":     (0.20, 0.10),
        "instrumentalness": (0.03, 0.04),
        "liveness":         (0.13, 0.06),
        "speechiness":      (0.08, 0.03),
        "loudness":         (-8.5, 1.9),
        "tempo":            (130,  17),
    },
    "The Queen Is Dead": {
        "energy":           (0.62, 0.15),
        "danceability":     (0.52, 0.11),
        "valence":          (0.32, 0.13),
        "acousticness":     (0.22, 0.12),
        "instrumentalness": (0.02, 0.03),
        "liveness":         (0.12, 0.05),
        "speechiness":      (0.09, 0.04),
        "loudness":         (-8.0, 1.7),
        "tempo":            (135,  19),
    },
    "Strangeways, Here We Come": {
        "energy":           (0.50, 0.13),
        "danceability":     (0.45, 0.10),
        "valence":          (0.28, 0.11),
        "acousticness":     (0.35, 0.14),
        "instrumentalness": (0.03, 0.04),
        "liveness":         (0.11, 0.05),
        "speechiness":      (0.07, 0.03),
        "loudness":         (-9.1, 2.0),
        "tempo":            (118,  16),
    },
}


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def rand_feat(mean, std, lo=0.0, hi=1.0):
    return round(clamp(random.gauss(mean, std), lo, hi), 4)


tracks = []
tid = 1
for album in ALBUMS:
    aname = album["name"]
    prof = PROFILES[aname]
    for i, tname in enumerate(TRACKS[aname]):
        dur_ms = int(clamp(random.gauss(200000, 45000), 90000, 420000))
        track = {
            "id": f"sm_{tid:04d}",
            "name": tname,
            "album": aname,
            "release_date": album["release_date"],
            "year": album["year"],
            "track_number": i + 1,
            "duration_ms": dur_ms,
            "duration_min": round(dur_ms / 60000, 2),
            "danceability":     rand_feat(*prof["danceability"]),
            "energy":           rand_feat(*prof["energy"]),
            "valence":          rand_feat(*prof["valence"]),
            "acousticness":     rand_feat(*prof["acousticness"]),
            "instrumentalness": rand_feat(prof["instrumentalness"][0], prof["instrumentalness"][1], 0.0, 0.99),
            "liveness":         rand_feat(*prof["liveness"]),
            "speechiness":      rand_feat(*prof["speechiness"]),
            "loudness":         round(random.gauss(prof["loudness"][0], prof["loudness"][1]), 3),
            "tempo":            round(clamp(random.gauss(prof["tempo"][0], prof["tempo"][1]), 60, 200), 3),
            "key":              random.randint(0, 11),
            "mode":             random.randint(0, 1),
            "time_signature":   4,
            "explicit":         False,
        }
        tracks.append(track)
        tid += 1

FEAT_COLS = ["danceability", "energy", "valence", "acousticness",
             "instrumentalness", "liveness", "speechiness"]

albums_out = []
for i, album in enumerate(ALBUMS):
    aname = album["name"]
    atracks = [t for t in tracks if t["album"] == aname]
    means = {f: round(sum(t[f] for t in atracks) / len(atracks), 4) for f in FEAT_COLS}
    albums_out.append({
        "album_id": f"sm_album_{i+1:02d}",
        "name": aname,
        "release_date": album["release_date"],
        "year": album["year"],
        "total_tracks": len(atracks),
        "album_type": "album",
        **means,
        "mean_loudness": round(sum(t["loudness"] for t in atracks) / len(atracks), 3),
        "mean_tempo":    round(sum(t["tempo"]    for t in atracks) / len(atracks), 3),
    })


def stats_of(vals):
    n = len(vals)
    mean = sum(vals) / n
    std = math.sqrt(sum((v - mean) ** 2 for v in vals) / n)
    return {
        "mean": round(mean, 4), "std": round(std, 4),
        "min": round(min(vals), 4), "max": round(max(vals), 4),
    }


feat_stats = {f: stats_of([t[f] for t in tracks]) for f in FEAT_COLS}

data_dir = Path(__file__).parent
(data_dir / "smiths_tracks.json").write_text(
    json.dumps(tracks, indent=2), encoding="utf-8"
)
(data_dir / "smiths_albums.json").write_text(
    json.dumps(albums_out, indent=2), encoding="utf-8"
)
(data_dir / "smiths_stats.json").write_text(
    json.dumps({
        "artist": "The Smiths",
        "total_tracks": len(tracks),
        "total_albums": len(albums_out),
        "albums": [a["name"] for a in albums_out],
        "year_range": [1984, 1987],
        "features": feat_stats,
    }, indent=2), encoding="utf-8"
)

print(f"Generated {len(tracks)} tracks, {len(albums_out)} albums")
print("Saved: smiths_tracks.json, smiths_albums.json, smiths_stats.json")
