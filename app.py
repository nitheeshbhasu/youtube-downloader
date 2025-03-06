import yt_dlp

def download_playlist(url):
    ydl_opts = {
        "format": "bv*[height=720]+ba/best",  # Select 1080p video and best audio
        "merge_output_format": "mp4",  # Ensure MP4 output
        "outtmpl": "%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s",  # Organize into playlist folder
        "noplaylist": False,  # Allow playlist downloading
        "retries": 10,  # Retry up to 10 times for failed downloads;
        "fragment_retries": 10,  # Retry failed video fragments
        "continue": True,  # Resume interrupted downloads
        "ignoreerrors": True,  # Skip failed videos instead of stopping
        "buffersize": 16 * 1024,  # Set buffer size to 16 KB for stability
        "postprocessors": [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",  # Convert output to MP4
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    playlist_url = input("Enter YouTube Playlist URL: ")
    download_playlist(playlist_url)
