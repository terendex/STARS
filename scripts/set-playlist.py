"""Chooses the music the mission clock plays (ctfd-plugin/assets/playlist.json).

Give it a Spotify album or playlist link. It reads the public embed page, which
lists the tracks, so no Spotify account or API key is needed here:

    python scripts/set-playlist.py https://open.spotify.com/album/0HmBQ2vhh1fT3kaBi92Bip

Run it with your own Python, not inside Docker, because the CTF's containers
have no internet. The clock page shuffles the tracks every time the clock starts.
The CTFd containers read the plugin folder directly, so a browser refresh of
/timer picks up the new list.
"""
import json
import pathlib
import re
import sys
import urllib.request

OUT = pathlib.Path(__file__).resolve().parent.parent / "ctfd-plugin" / "assets" / "playlist.json"

if len(sys.argv) != 2:
    sys.exit(__doc__)
match = re.search(r"open\.spotify\.com/(?:intl-[a-z-]+/)?(album|playlist)/([A-Za-z0-9]{22})", sys.argv[1])
if not match:
    sys.exit("That doesn't look like a Spotify album or playlist link.")
kind, spotify_id = match.groups()

request = urllib.request.Request(
    f"https://open.spotify.com/embed/{kind}/{spotify_id}",
    headers={"User-Agent": "Mozilla/5.0"},
)
html = urllib.request.urlopen(request, timeout=30).read().decode("utf-8")
data = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html, re.S)
if not data:
    sys.exit("Spotify's embed page has changed, so the track list couldn't be read.")
entity = json.loads(data.group(1))["props"]["pageProps"]["state"]["data"]["entity"]

tracks = [
    {"uri": track["uri"], "title": track["title"], "artist": track.get("subtitle", "").replace("\xa0", " ")}
    for track in entity["trackList"]
    if track.get("isPlayable", True) and track["uri"].startswith("spotify:track:")
]
if not tracks:
    sys.exit("No playable tracks found.")

playlist = {
    "name": entity.get("name", ""),
    "by": entity.get("subtitle", "").replace("\xa0", " "),
    "link": f"https://open.spotify.com/{kind}/{spotify_id}",
    "tracks": tracks,
}
OUT.write_text(json.dumps(playlist, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
print(f"{len(tracks)} tracks from {playlist['name']} ({playlist['by']}) written to {OUT.name}.")
