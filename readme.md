# Deezer to YouTube Music Downloader

The problem -> i needed to download .mp3 for my ancient iPod shuffle (which still works after 20 years) fromb my (public) Deezer playlist.

## Project Description
A Python script that:
1. Fetches songs from a Deezer playlist
2. Searches for matching songs on YouTube using Brave API
3. Downloads the found YouTube videos as audio files

## Requirements
- Python 3.x
- Deezer API access
- Brave API key for search functionality
- YouTube video downloader library (e.g., yt-dlp)

## Input Requirements
- Deezer playlist URL/ID
- BRAVE_API_KEY environment variable
- Output directory for downloaded songs

## Expected Features
- Extract song details (title, artist) from Deezer playlist
- Search YouTube using Brave API to find matching songs
- Download highest quality audio from YouTube videos
- Handle errors and retries
- Progress tracking
- Basic audio format conversion

## Nice-to-have Features
- Audio metadata tagging
- Duplicate detection
- Parallel downloads
- Resume capability
- Quality/match verification

## Technical Considerations
- Rate limiting for APIs
- Error handling
- File naming conventions
- Audio quality preferences

# Instructions

1. Install Python 3.x
2. Install yt-dlp
3. Install requests
4. Install python-dotenv
5. Set BRAVE_API_KEY environment variable (create .env or rename .env.example file with BRAVE_API_KEY="your_brave_api_key")

So input parameter will be URL to deezer playlist and output directoy will contain .mp3 files with "artist - title" format.

Recommended to create a virtual environment and install dependencies there.


## Example of use

```cmd
python deezer2yt.py "https://www.deezer.com/us/playlist/123456789" ./music-output
```


# License

MIT

# Author
Matija 

# Bugs and suggestions
Please create an issue on GitHub.