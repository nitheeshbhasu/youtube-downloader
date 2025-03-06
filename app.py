import streamlit as st
import yt_dlp
import os
import tempfile


# Load custom CSS
def load_css(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Load styles.css
load_css("yt1.css")

# Get default Downloads folder
default_download_path = os.path.join(os.path.expanduser("~"), "Downloads")


def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d['_percent_str']
        st.write(f"📊 Download Progress: {percent}")


def download_playlist(url, resolution, download_path):
    output_path = os.path.join(download_path, "%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s")

    ydl_opts = {
        "format": f"bv*[height={resolution.rstrip('p')}]+ba/best",
        "merge_output_format": "mp4",
        "outtmpl": output_path,
        "noplaylist": False,
        "retries": 10,
        "fragment_retries": 10,
        "continue": True,
        "ignoreerrors": True,
        "buffersize": 16 * 1024,
        "progress_hooks": [progress_hook],
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return output_path


# 🎨 Streamlit UI
st.title("🎥 YouTube Playlist Downloader 🚀")
st.subheader("📥 Download your favorite YouTube playlists in any resolution!")

# Select Device Type
device_type = st.radio("📱💻 Select Device:", ["Mobile", "PC"], index=0)

# 🎯 User Inputs
playlist_url = st.text_input("🔗 Enter YouTube Playlist URL:")
resolution = st.selectbox(
    "🎚️ Select Video Resolution:",
    ["144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"],
    index=4
)

# Show selected resolution
if resolution:
    st.write(f"✅ Selected Resolution: **{resolution}**")

download_path = ""
if device_type == "PC":
    download_path = st.text_input("📂 Enter Download Folder Path:", default_download_path)

# ✅ Download Button
if st.button("🚀 Start Download"):
    if playlist_url:
        final_path = download_path if device_type == "PC" and download_path else tempfile.gettempdir()
        if device_type == "PC" and not os.path.exists(final_path):
            os.makedirs(final_path)

        st.write(f"⏳ Downloading in **{resolution}** resolution... Please wait! 🎬")
        try:
            file_path = download_playlist(playlist_url, resolution, final_path)
            st.success(f"✅ Download complete! Check your folder: **{final_path}** 🎉")

            # Provide download button for mobile users
            if device_type == "Mobile":
                with open(file_path, "rb") as file:
                    st.download_button("📥 Download Video", file, file_name="video.mp4")

        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.error("❌ Please enter a valid YouTube Playlist URL! 🔗")

# 📌 Footer
st.markdown("📢 **Tip:** Higher resolutions (1080p+) may take longer to download. 🚀")
