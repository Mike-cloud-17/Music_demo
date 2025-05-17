"""
Мини-рекомендер для демо-MVP.

* Достаём превью-плеер из **Spotify** (если нашли трек)
* Видео-клип — из YouTube.
"""

from __future__ import annotations
import random, urllib.parse as up, requests
from dataclasses import dataclass
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# ──────────────────────────────
# 1) API-ключи / константы
# ──────────────────────────────
YT_KEY           = "AIzaSyAUuTaeOfmyd2SSK5NGYjUg116IcQDGFXU"
SPOTIFY_ID       = "6747cde4ba754852b835b7f92e781a49"
SPOTIFY_SECRET   = "0b9eca81195942788c6cca1343a096f2"

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_ID,
        client_secret=SPOTIFY_SECRET
    )
)

SEEDS = [
    "Never Gonna Give You Up Rick Astley",
    "Daft Punk Harder Better Faster Stronger",
    "Nirvana Smells Like Teen Spirit",
    "Billie Eilish bad guy",
    "Coldplay Viva La Vida",
    "Queen Bohemian Rhapsody",
    "A-ha Take On Me",
    "Avicii Wake Me Up",
    "Linkin Park Numb",
    "ABBA Dancing Queen",
]

DEFAULT_COVER = "https://i.imgur.com/Z8l0XUJ.jpeg"


@dataclass
class Track:
    title:  str
    artist: str
    genre:  str
    sp_url: str | None   # Spotify iframe
    yt_url: str | None   # YouTube iframe
    cover:  str


# ──────────────────────────────
# 2) util-функции к API
# ──────────────────────────────
def _spotify(query: str) -> tuple[str, str | None, str]:
    """
    Ищет трек → (title, iframe-src | None, cover_url)
    """
    try:
        res = sp.search(q=query, type="track", limit=1)
        if not res["tracks"]["items"]:
            return query, None, DEFAULT_COVER
        trk  = res["tracks"]["items"][0]
        tid  = trk["id"]
        cover = trk["album"]["images"][0]["url"] if trk["album"]["images"] else DEFAULT_COVER
        iframe = f"https://open.spotify.com/embed/track/{tid}?utm_source=generator"
        return trk["name"], iframe, cover
    except Exception as e:
        print("Spotify error:", e)
        return query, None, DEFAULT_COVER


def _youtube(query: str, region="US") -> str | None:
    api = (
        "https://www.googleapis.com/youtube/v3/search?"
        "part=snippet&type=video&videoEmbeddable=true&maxResults=5"
        f"&q={up.quote(query)}&key={YT_KEY}&regionCode={region}"
    )
    try:
        items = requests.get(api, timeout=8).json().get("items", [])
        for it in items:
            vid = it["id"]["videoId"]
            return f"https://www.youtube.com/embed/{vid}"
        return None
    except Exception as e:
        print("YouTube error:", e)
        return None


# ──────────────────────────────
# 3) «Модель»-карусель
# ──────────────────────────────
class RealRecommender:
    def __init__(self) -> None:
        self.catalog = [self._make(seed) for seed in SEEDS]
        random.shuffle(self.catalog)
        self.pos = 0

    def _make(self, seed: str) -> Track:
        title, sp_src, cover = _spotify(seed)
        yt_src = _youtube(seed)
        artist = seed.split()[-1]
        return Track(title, artist, "Pop/Rock", sp_src, yt_src, cover)

    # — публичные —
    def _cur(self) -> Track:
        return self.catalog[self.pos]

    def next(self) -> Track:
        self.pos = (self.pos + 1) % len(self.catalog)
        return self._cur()

    def next_track(self) -> dict:      # для AJAX
        t = self.next()
        return t.__dict__

    def by_genre(self, genre: str) -> dict:
        return self.next_track()

    def like(self) -> None:     pass
    def dislike(self) -> None:  pass
