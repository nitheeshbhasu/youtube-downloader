import streamlit as st
import yt_dlp
import os
import tempfile



# Load custom CSS
def load_css(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

        # Load CSS file
        load_css("yt1.css")


# Get default Downloads folder
default_download_path = os.path.join(os.path.expanduser("~"), "Downloads")


# Function to format speed
def format_speed(speed):
    if speed is None:
        return "Unknown"
    elif speed < 1024:
        return f"{speed} B/s"
    elif speed < 1024 ** 2:
        return f"{speed / 1024:.2f} KB/s"
    else:
        return f"{speed / 1024 ** 2:.2f} MB/s"

# Function to format size
def format_size(size):
    if size is None:
        return "Unknown"
    elif size < 1024:
        return f"{size} B"
    elif size < 1024 ** 2:
        return f"{size / 1024:.2f} KB"
    elif size < 1024 ** 3:
        return f"{size / 1024 ** 2:.2f} MB"
    else:
        return f"{size / 1024 ** 3:.2f} GB"

# Function to download playlist with progress tracking
def download_playlist(url, resolution, download_path):
    def progress_hook(d):
        if d['status'] == 'downloading':
            percentage = (d.get('downloaded_bytes', 0) / d.get('total_bytes', 1)) * 100
            st.session_state.progress_bar.progress(percentage / 100)
            st.session_state.progress_text.text(f"Downloaded: {percentage:.2f}%")
            st.session_state.speed_text.text(f"Speed: {format_speed(d.get('speed', 0))}")
            st.session_state.size_text.text(
                f"Size: {format_size(d.get('downloaded_bytes', 0))} / {format_size(d.get('total_bytes', 0))}")
        elif d['status'] == 'finished':
            st.session_state.progress_bar.progress(1)
            st.session_state.progress_text.text("✅ Download complete!")

    # Ensure the directory exists
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Set output template
    output_path = os.path.join(download_path, "%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s")

    # Updated format options to bypass restrictions
    ydl_opts = {
        "format": f"bv*[height<={resolution.rstrip('p')}]+ba/best",
        "merge_output_format": "mp4",
        "outtmpl": output_path,
        "noplaylist": False,
        "retries": 10,
        "progress_hooks": [progress_hook],
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "cookies-from-browser": "chrome",  # Bypass authentication issues
        "force_generic_extractor": True,  # Fix some 403 errors
        # "proxy": "http://your-proxy-address:port"  # Uncomment & replace if needed
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return output_path

# Streamlit UI
def main():
    st.title("📺 YouTube Playlist Downloader 🎓")
    st.info("⚠️ **Note:** Works on **PC & Mobile**")

    # Select device type
    device_type = st.radio("📱💻 Select Device:", ["Mobile", "PC"], index=0)

    # User inputs
    playlist_url = st.text_input("🔗 Enter YouTube Playlist URL:")

    # Updated resolution list
    resolution = st.selectbox(
        "🎥 Select Resolution:",
        ["144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p (4K)"],
        index=5
    )

    # Select Download Path
    download_path = ""
    if device_type == "PC":
        default_download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        download_path = st.text_input("📂 Enter Download Folder Path:", default_download_path)

    # Initialize progress tracking
    st.session_state.progress_bar = st.progress(0)
    st.session_state.progress_text = st.empty()
    st.session_state.speed_text = st.empty()
    st.session_state.size_text = st.empty()

    # Download Button
    if st.button("🚀 Start Download"):
        if playlist_url:
            final_path = download_path if device_type == "PC" and download_path else tempfile.gettempdir()

            # Ensure directory exists before downloading
            if not os.path.exists(final_path):
                os.makedirs(final_path)

            st.write(f"⏳ Downloading in **{resolution}** resolution... Please wait! 🎬")
            try:
                file_path = download_playlist(playlist_url, resolution, final_path)
                st.success(f"✅ Download complete! Check your folder: **{final_path}** 🎉")

                # Mobile download button
                if device_type == "Mobile":
                    with open(file_path, "rb") as file:
                        st.download_button("📥 Download Video", file, file_name="video.mp4")

            except Exception as e:
                st.error(f"❌ Error: {e}")
        else:
            st.error("❌ Please enter a valid YouTube Playlist URL! 🔗")

    # Sidebar
    st.sidebar.subheader("👨🏻‍💻 Developed By")
    st.sidebar.subheader("⚡ Nitheesh K A")
    st.sidebar.subheader("📚 Educational Purpose Only")
    st.sidebar.subheader("⚠️ Disclaimer")
    st.sidebar.info(
        "1. Copyright Compliance: Use for educational/personal use only.\n"
        "2. Responsibility: The developer is not responsible for any content downloaded.\n"
        "3. Content Ownership: Intended for publicly available videos.\n"
        "4. No Liability: Use at your own risk.\n"
        "5. Terms of Service: Comply with the terms of any platform you download from."
    )

if __name__ == "__main__":
    main()
