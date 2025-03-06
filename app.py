import streamlit as st
import yt_dlp

def download_playlist(url, quality):
    ydl_opts = {
        "format": f"bv*[height={quality}]+ba/best",  # Select the chosen resolution
        "merge_output_format": "mp4",  # Ensure MP4 output
        "outtmpl": "%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s",  # Organize into playlist folder
        "noplaylist": False,  # Allow playlist downloading
        "retries": 10,  # Retry up to 10 times for failed downloads
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

# Streamlit UI
st.title("YouTube Playlist Downloader")

playlist_url = st.text_input("Enter YouTube Playlist URL:")
quality = st.selectbox("Select Video Quality:", ["144", "240", "360", "480", "720", "1080", "1440", "2160"], index=5)

if st.button("Download Playlist"):
    if playlist_url:
        st.write(f"Downloading playlist in {quality}p...")
        download_playlist(playlist_url, quality)
        st.success("Download complete!")
    else:
        st.error("Please enter a valid YouTube Playlist URL.")
