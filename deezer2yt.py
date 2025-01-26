import os
import re
import argparse
import requests
import time
import yt_dlp
from urllib.parse import urlparse

# Basic filename sanitization
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)

# Fetch all tracks from Deezer playlist with pagination
def fetch_deezer_playlist_tracks(playlist_id):
    tracks = []
    url = f"https://api.deezer.com/playlist/{playlist_id}/tracks"
    while url:
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            tracks.extend(data["data"])
            url = data.get("next")
            time.sleep(0.5)  # Rate limiting
        except Exception as e:
            print(f"Error fetching Deezer tracks: {e}")
            break
    return tracks

# Search YouTube using Brave API
def search_youtube_video(query, brave_api_key):
    headers = {"Accept": "application/json", "X-Subscription-Token": brave_api_key}
    params = {"q": f"{query} site:youtube.com", "count": 3}
    
    try:
        response = requests.get(
            "https://api.search.brave.com/res/v1/web/search",
            headers=headers,
            params=params
        )
        response.raise_for_status()
        results = response.json().get("web", {}).get("results", [])
        
        for result in results:
            url = result.get("url", "")
            if "youtube.com/watch" in url:
                return url
    except Exception as e:
        print(f"Brave search failed: {e}")
    
    return None

def main():
    parser = argparse.ArgumentParser(description="Deezer to YouTube Music Downloader")
    parser.add_argument("playlist_url", help="Deezer playlist URL")
    parser.add_argument("output_dir", help="Output directory for MP3 files")
    args = parser.parse_args()

    # Validate and create output directory
    os.makedirs(args.output_dir, exist_ok=True)

    # Extract Deezer playlist ID - updated regex to handle language codes
    match = re.search(r"deezer\.com/[a-z]{2}/playlist/(\d+)", args.playlist_url)
    if not match:
        print("Invalid Deezer playlist URL")
        return
    playlist_id = match.group(1)

    # Get Brave API key
    brave_api_key = os.getenv("BRAVE_API_KEY")
    if not brave_api_key:
        print("BRAVE_API_KEY environment variable not set")
        return

    # Fetch Deezer playlist tracks
    print(f"Fetching tracks from Deezer playlist {playlist_id}...")
    tracks = fetch_deezer_playlist_tracks(playlist_id)
    if not tracks:
        print("No tracks found in playlist")
        return

    print(f"Found {len(tracks)} tracks, starting downloads...")

    # Process each track
    for i, track in enumerate(tracks, 1):
        artist = track["artist"]["name"]
        title = track["title"]
        sanitized_artist = sanitize_filename(artist)
        sanitized_title = sanitize_filename(title)
        filename = f"{sanitized_artist} - {sanitized_title}.mp3"
        filepath = os.path.join(args.output_dir, filename)

        # Skip existing files
        if os.path.exists(filepath):
            print(f"[{i}/{len(tracks)}] Skipping existing: {filename}")
            continue

        print(f"[{i}/{len(tracks)}] Processing: {artist} - {title}")

        # Search YouTube
        yt_url = None
        for attempt in range(3):
            yt_url = search_youtube_video(f"{artist} - {title}", brave_api_key)
            if yt_url:
                break
            time.sleep(1)
        
        if not yt_url:
            print(f"  No YouTube video found after 3 attempts")
            continue

        # Download audio with yt-dlp
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(args.output_dir, f"{sanitized_artist} - {sanitized_title}.%(ext)s"),
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "quiet": True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([yt_url])
            print(f"  Downloaded: {filename}")
        except Exception as e:
            print(f"  Download failed: {e}")

        time.sleep(1)  # Rate limiting between downloads

if __name__ == "__main__":
    main()