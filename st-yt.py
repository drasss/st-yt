import pytubefix as pytube
import streamlit as st


# PAGE CONFIG
st.set_page_config(layout="wide",
                   page_title="yt",
                   page_icon="content/yt.ico",
                   initial_sidebar_state="collapsed")

src,o=st.tabs(["Search","watch"])

#------------------ side bar parameters

#lg=st.sidebar.selectbox("Language",["fr","en"])
nbr=st.sidebar.slider("Number of results",2,80,value=5)
# --- Functions

def yt_watch(url):
    """Open a YouTube video in a new tab."""
    global o
    k=o.video(url)

def yt_search(query, nbr=nbr):
    """Search for videos on YouTube and display results."""
    ct=[]
    cl=[]
    i=0
    search_results = pytube.Search(query)
    if search_results.videos:
        #limit the number of results to nbr

        search_results_limited = search_results.videos[:nbr]
        for video in search_results_limited:
            # Display video information
            if i%4 == 0:
                ct.append(src.container())
                cl.append(src.columns([1,1,1,1]))
            cl[-1][i%4].write(f"**Title:** {video.title}")
            cl[-1][i%4].button("Watch", on_click=yt_watch, args=(video.watch_url,), type="primary",key=video.video_id)
            cl[-1][i%4].image(video.thumbnail_url, width=200)
            i+=1
        # Display the total number of results
        src.write(f"Total results found: {len(search_results.videos)}")
    else:
        src.error("No results found.")


#---------------------- main page : watch

#---------------------- main page : search
para=src.columns([10,100])


choice=para[1].text_input("Youtube search")
launch=para[0].button("Search",on_click=yt_search,args=(choice,nbr),type="primary")



        
