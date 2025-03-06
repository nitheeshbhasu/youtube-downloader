import streamlit as st
import yt_dlp
import os

# Load custom CSS
def load_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load styles.css
load_css("yt1.css")

# Get default Downloads folder
default_download_path = os.path.join(os.path.expanduser("~"), "Downloads")


def download_playlist(url, resolution, download_path):
    ydl_opts = {
        "format": f"bv*[height={resolution}]+ba/best",
        "merge_output_format": "mp4",
        "outtmpl": os.path.join(download_path, "%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s"),
        "noplaylist": False,
        "retries": 10,
        "fragment_retries": 10,
        "continue": True,
        "ignoreerrors": True,
        "buffersize": 16 * 1024,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


# 🎨 Streamlit UI
st.title("🎥 YouTube Playlist Downloader 🚀")
st.subheader("📥 Download your favorite YouTube playlists in any resolution!")

# 🎯 User Inputs
playlist_url = st.text_input("🔗 Enter YouTube Playlist URL:")
resolution = st.selectbox(
    "🎚️ Select Video Resolution:",
    ["144", "240", "360", "480", "720", "1080", "1440", "2160"],
    index=4
)

download_path = st.text_input("📂 Enter Download Folder Path (Optional):", default_download_path)

# ✅ Download Button
if st.button("🚀 Start Download"):
    if playlist_url:
        final_path = download_path if download_path else default_download_path
        if not os.path.exists(final_path):
            os.makedirs(final_path)

        st.write(f"⏳ Downloading in **{resolution}p** resolution... Please wait! 🎬")
        download_playlist(playlist_url, resolution, final_path)
        st.success(f"✅ Download complete! Check your folder: **{final_path}** 🎉")
    else:
        st.error("❌ Please enter a valid YouTube Playlist URL! 🔗")

# 📌 Footer
st.markdown("📢 **Tip:** Higher resolutions (1080p+) may take longer to download. 🚀")
