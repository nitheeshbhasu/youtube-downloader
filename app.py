import yt_dlp
import streamlit as st
import os


# Load custom CSS
def load_css(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

        # Load CSS file
        load_css("yt1.css")

# Get default Downloads folder
default_download_path = os.path.join(os.path.expanduser("~"), "Downloads")

# Function to download the playlist with progress
def download_playlist(url, resolution, download_path):
    # Progress hook to track download progress
    def progress_hook(d):
        downloaded_bytes = d.get('downloaded_bytes', 0)
        total_bytes = d.get('total_bytes', 0)
        speed = d.get('speed', 0)

        if d['status'] == 'downloading':
            percentage = (downloaded_bytes / total_bytes) * 100 if total_bytes > 0 else 0
            st.session_state.progress_bar.progress(percentage / 100)
            st.session_state.progress_text.text(f"Downloaded: {percentage:.2f}%")
            st.session_state.speed_text.text(f"Speed: {format_speed(speed)}")
            st.session_state.size_text.text(f"Downloaded: {format_size(downloaded_bytes)} / Total Size: {format_size(total_bytes)}")
        elif d['status'] == 'finished':
            st.session_state.progress_bar.progress(1)
            st.session_state.progress_text.text("Download complete!")

    def format_speed(speed):
        if speed is None:
            return "Unknown"
        elif speed < 1024:
            return f"{speed} B/s"
        elif speed < 1024**2:
            return f"{speed / 1024:.2f} KB/s"
        else:
            return f"{speed / 1024**2:.2f} MB/s"

    def format_size(size):
        if size is None:
            return "Unknown"
        elif size < 1024:
            return f"{size} B"
        elif size < 1024**2:
            return f"{size / 1024:.2f} KB"
        elif size < 1024**3:
            return f"{size / 1024**2:.2f} MB"
        else:
            return f"{size / 1024**3:.2f} GB"

    # Download options
    ydl_opts = {
        "format": f"bv*[height<={resolution.rstrip('p')}] + ba/best",
        "merge_output_format": "mp4",
        "outtmpl": os.path.join(download_path, "%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s"),
        "noplaylist": False,
        "retries": 10,
        "fragment_retries": 10,
        "continue": True,
        "ignoreerrors": True,
        "progress_hooks": [progress_hook],
        "postprocessors": [{"key": "FFmpegMerger"}],
        "ffmpeg_location": "./ffmpeg/bin"
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        st.success("✅ Download complete! Check your folder.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Streamlit UI
def main():
    st.title("📺 YouTube Video/Playlist Downloader 🎓")
    st.info("Works on PC & Mobile")

    playlist_url = st.text_input("🔗 Enter YouTube Playlist URL:")
    resolution = st.selectbox("🎥 Select Resolution:", ["144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p (4K)"])
    download_path = st.text_input("📂 Enter Download Path:", value=os.getcwd())

    # Initialize progress components
    st.session_state.progress_bar = st.progress(0)
    st.session_state.progress_text = st.empty()
    st.session_state.speed_text = st.empty()
    st.session_state.size_text = st.empty()

    if st.button("Download"):
        if playlist_url and download_path:
            if not os.path.exists(download_path):
                os.makedirs(download_path)
            st.write(f"Downloading at {resolution} to {download_path}")
            download_playlist(playlist_url, resolution, download_path)
        else:
            st.error("Please enter a valid Playlist URL and Download Path.")

    st.sidebar.subheader("👨🏻‍💻 Developed By Jashwanth Raj J.R")
    st.sidebar.subheader("📚 Educational Purpose Only")
    st.sidebar.info("Use responsibly and comply with platform terms.")

if __name__ == "__main__":
    main()
