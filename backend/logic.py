# backend/logic.py
"""
Мини-рекомендер для демо-MVP  
• превью-плеер — Spotify  
• клип       — VK Video (URL-ы пока пустые — добавите сами)
"""
from __future__ import annotations
import random
from dataclasses import dataclass
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# ─── 1. CONSTANTS ───────────────────────────────────────
SPOTIFY_ID     = "6747cde4ba754852b835b7f92e781a49"
SPOTIFY_SECRET = "0b9eca81195942788c6cca1343a096f2"

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_ID,
        client_secret=SPOTIFY_SECRET,
    )
)

# 4 трека: первые два — Rock, 3-й — Pop, 4-й — Pop
SEEDS = [
    "Queen Bohemian Rhapsody",
    "AC/DC Back in Black",
    "Michael Jackson Billie Jean",
    "Madonna Like a Prayer",
]

# принудительные жанры, чтобы контролировать порядок
_GENRE = {
    "queen bohemian rhapsody":    "Rock",
    "ac/dc back in black":        "Rock",
    "michael jackson billie jean":"Pop",
    "madonna like a prayer":      "Pop",
}

# VK-iframe — заполните своими ссылками
_VK_OVERRIDE: dict[str, str] = {
    "queen bohemian rhapsody":
        "https://vk.com/video_ext.php?oid=-227373631&id=456239954&hd=0",
    "ac/dc back in black":
        "https://vk.com/video_ext.php?oid=-227373812&id=456239180&hd=0",
    "michael jackson billie jean":
        "https://vkvideo.ru/video_ext.php?oid=-137961550&id=456241080&hd=2&autoplay=1",
    "madonna like a prayer":
        "https://vkvideo.ru/video_ext.php?oid=-16980751&id=456245638&hd=1&autoplay=1",
}

DEFAULT_COVER = "https://i.imgur.com/Z8l0XUJ.jpeg"

@dataclass
class Track:
    title:  str
    artist: str
    genre:  str
    sp_url: str | None
    vk_url: str | None
    cover:  str

# ─── 2. helpers ─────────────────────────────────────────
def _spotify(query: str) -> tuple[str, str | None, str]:
    """Spotify search → (title, iframe|None, cover)"""
    try:
        items = sp.search(q=query, type="track", limit=1)["tracks"]["items"]
        if not items:
            return query, None, DEFAULT_COVER
        trk    = items[0]
        tid    = trk["id"]
        cover  = (trk["album"]["images"][0]["url"]
                  if trk["album"]["images"] else DEFAULT_COVER)
        iframe = f"https://open.spotify.com/embed/track/{tid}?utm_source=generator"
        return trk["name"], iframe, cover
    except Exception as e:
        print("Spotify error:", e)
        return query, None, DEFAULT_COVER

def _vk(query: str) -> str | None:
    return _VK_OVERRIDE.get(query.lower())

# ─── 3. Recommender ─────────────────────────────────────
class RealRecommender:
    def __init__(self) -> None:
        self.catalog = [self._make(seed) for seed in SEEDS]
        self.pos = 0  # порядок фиксированный, без shuffle

    def _make(self, seed: str) -> Track:
        title, sp_url, cover = _spotify(seed)
        vk_url               = _vk(seed)
        genre                = _GENRE[seed.lower()]
        artist               = seed.split(None, 1)[0]
        return Track(title, artist, genre, sp_url, vk_url, cover)

    # — публичные —
    def _cur(self) -> Track:
        return self.catalog[self.pos]

    def next(self) -> Track:
        self.pos = (self.pos + 1) % len(self.catalog)
        return self._cur()

    def next_track(self) -> dict:
        return self.next().__dict__

    def by_genre(self) -> dict:
        # следующий трек того же жанра, что и текущий
        current_genre = self._cur().genre
        start = self.pos
        while True:
            self.next()
            if self._cur().genre == current_genre or self.pos == start:
                break
        return self._cur().__dict__

    def like(self):    pass
    def dislike(self): pass
