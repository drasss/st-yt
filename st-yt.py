import pytubefix as pytube
import streamlit as st


# PAGE CONFIG
st.set_page_config(layout="wide",
                   page_title="yt",
                   page_icon="content/yt.ico",
                   initial_sidebar_state="collapsed")

src,o=st.tabs(["Search","watch"])

#------------------ side bar parameters
url_cv= st.sidebar.text_input("YouTube video URL", placeholder="Enter YouTube video URL here")
choice_cv = st.sidebar.selectbox("Conversion Type", ["Audio", "Video","thumbnail"])
if st.sidebar.button("Convert"):
    content=pytube.Search(url_cv)
    if content.videos:
        if choice_cv == "Audio":   
            # Convert to audio
            video = content.videos[0]
            audio_stream = video.streams.get_audio_only()
            st.sidebar.download_button("Download Audio",
                                       data=audio_stream.download(filename=f"{video.title}.mp3"),
                                       file_name=f"{video.title}.mp3",
                                       mime="audio/mpeg")
            st.sidebar.success(f"Audio downloaded: {video.title}.mp3")
        elif choice_cv == "Video":
            # Convert to video
            video = content.videos[0]
            video_stream = video.streams.get_highest_resolution()
            st.sidebar.download_button("Download Video",
                                       data=video_stream.download(filename=f"{video.title}.mp4"),
                                       file_name=f"{video.title}.mp4",
                                       mime="video/mp4")
            st.sidebar.success(f"Video downloaded: {video.title}.mp4")
        elif choice_cv == "thumbnail":
            # Download thumbnail
            video = content.videos[0]
            st.sidebar.image(video.thumbnail_url, caption="Thumbnail", use_column_width=True)
            st.sidebar.download_button("Download Thumbnail",
                                       data=video.thumbnail_url,
                                       file_name=f"{video.title}_thumbnail.jpg",
                                       mime="image/jpeg")
            st.sidebar.success(f"Thumbnail downloaded: {video.title}_thumbnail.jpg")
        st.sidebar.error("Please enter a valid YouTube URL.")


# --- Functions

def yt_watch(url):
    """Open a YouTube video in a new tab."""
    global o
    o.video(url)

def yt_search(query, lg="en", nbr=10):
    """Search for videos on YouTube and display results."""

    search_results = pytube.Search(query)
    if search_results.videos:
        #limit the number of results to nbr
        search_results_limited = search_results.videos[:nbr]
        for video in search_results_limited:
            # Display video information
            src.write(f"**Title:** {video.title}")
            src.button("Watch", on_click=yt_watch, args=(video.watch_url,), type="primary",key=video.video_id)
            src.image(video.thumbnail_url, width=200)
            src.write("---")
        # Display the total number of results
        src.write(f"Total results found: {len(search_results.videos)}")
    else:
        src.error("No results found.")


#---------------------- main page : watch

#---------------------- main page : search
para=src.columns([10,100])
choice=para[1].text_input("Youtube search")
lg=para[0].selectbox("Language",["fr","en"])
nbr=para[0].slider("Number of results",2,80,value=10)

launch=para[0].button("Search",on_click=yt_search,args=(choice,lg,nbr),type="primary")

        
