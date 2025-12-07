import streamlit as st
from serpapi import GoogleSearch
import os
# from dotenv import load_dotenv # Not needed for Cloud

# Load environment variables
# load_dotenv() # Not needed for Cloud

# --- Page Config & Theme ---
st.set_page_config(
    page_title="Velvet News | Neo-Jazz Label",
    page_icon="🎷",
    layout="centered"
)

# --- Custom CSS (Neo-Jazzy Aesthetic) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Montserrat:wght@300;400;600&display=swap');

    /* Main Background */
    .stApp {
        background-color: #0c0f1d; /* Deep Midnight Blue */
        background-image: radial-gradient(circle at 50% 0%, #1a162e 10%, #0c0f1d 80%);
        color: #e0e0e0;
        font-family: 'Montserrat', sans-serif;
    }

    /* Headings */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #d4af37 !important; /* Brass/Gold */
        text-shadow: 2px 2px 4px rgba(0,0,0,0.6);
        font-weight: 700 !important;
    }
    
    h1 { font-size: 3.5rem !important; margin-bottom: 0.5rem !important; }
    h3 { font-size: 1.5rem !important; color: #bca05b !important; }

    /* Subtitle */
    .subtitle {
        font-family: 'Montserrat', sans-serif;
        font-weight: 300;
        font-size: 1.2rem;
        color: #a8a8b3;
        margin-bottom: 3rem;
        text-transform: uppercase;
        letter-spacing: 3px;
    }

    /* Input Field */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.05);
        color: #d4af37; /* Gold text */
        border: 1px solid #d4af37;
        border-radius: 4px;
        font-family: 'Playfair Display', serif;
        font-size: 1.2rem;
        padding: 10px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #fceda3;
        box-shadow: 0 0 10px rgba(212, 175, 55, 0.3);
    }

    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, #d4af37 0%, #a8862d 100%);
        color: #0c0f1d !important;
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
        border: none;
        border-radius: 30px;
        padding: 0.6rem 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.5);
        background: linear-gradient(135deg, #fceda3 0%, #c49f37 100%);
    }

    /* Results Cards */
    .news-card {
        background: rgba(30, 25, 40, 0.6);
        border-left: 3px solid #d4af37;
        padding: 20px;
        margin-bottom: 20px;
        border-radius: 0 8px 8px 0;
        transition: all 0.3s ease;
        backdrop-filter: blur(5px);
    }
    .news-card:hover {
        background: rgba(40, 35, 50, 0.7);
        transform: translateX(5px);
        box-shadow: -5px 0 15px rgba(212, 175, 55, 0.1);
    }
    .news-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.4rem;
        color: #fff;
        margin-bottom: 8px;
        text-decoration: none;
        display: block;
    }
    .news-title:hover {
        color: #d4af37;
        text-decoration: underline;
    }
    .news-meta {
        font-size: 0.9rem;
        color: #8f8f9e;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .source-badge {
        background-color: #2a1b3d;
        color: #d4af37;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 1px;
    }
    .date-text {
        font-style: italic;
    }

    /* Spinner */
    .stSpinner > div {
        border-top-color: #d4af37 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Header Section ---
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.markdown("<h1 style='text-align: center;'>THE SCOUT</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle' style='text-align: center;'>Underground News for the Modern Ear</p>", unsafe_allow_html=True)

st.markdown("---")

# --- Search Section ---
col_side_l, col_main, col_side_r = st.columns([1, 2, 1])

with col_main:
    # Default to "Liniker" if not provided, trying to read from file first
    default_artist = "Liniker"
    if os.path.exists("artist.txt"):
        try:
            with open("artist.txt", "r") as f:
                content = f.read().strip()
                if content:
                    default_artist = content
        except:
            pass

    artist_name = st.text_input("ENTER ARTIST NAME", key="artist_input", value=default_artist)
    
    search_button = st.button("SEARCH ARCHIVES")

# --- Logic Section ---

if search_button and artist_name:
    
    # Try to get API key from Streamlit Secrets (Cloud) or Environment (Local)
    try:
        api_key = st.secrets["SERPAPI_API_KEY"]
    except:
        api_key = os.getenv("SERPAPI_API_KEY")
    
    if not api_key or "your_api_key_here" in api_key:
        st.error("⚠️ ACCESS DENIED: Missing SERPAPI_API_KEY in configuration.")
        st.info("Did you add it to Streamlit Secrets? (Manage App -> Settings -> Secrets)")
    else:

        # Update the artist.txt file
        with open("artist.txt", "w") as f:
            f.write(artist_name)

        # Tabs for different search modes
        tab1, tab2 = st.tabs(["🗞️ NEWS ARCHIVES", "📸 SOCIAL FEED (IG)"])

        # --- Tab 1: Google News ---
        with tab1:
            with st.spinner(f"Scanning frequencies for {artist_name}..."):
                params = {
                    "engine": "google_news",
                    "q": artist_name,
                    "tbs": "qdr:m",  # Past month
                    "api_key": api_key
                }

                try:
                    search = GoogleSearch(params)
                    results = search.get_dict()
                    news_results = results.get("news_results", [])
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    if not news_results:
                        st.warning(f"No recent transmissions found for {artist_name}.")
                    else:
                        st.markdown(f"<h3 style='text-align: center; margin-bottom: 30px;'>LATEST TRANSMISSIONS ({len(news_results)})</h3>", unsafe_allow_html=True)
                        
                        for news in news_results:
                            title = news.get("title", "Unknown Title")
                            link = news.get("link", "#")
                            date = news.get("date", "Unknown Date")
                            source = news.get("source", {}).get("name", "Unknown Source")
                            
                            st.markdown(f"""
                            <div class="news-card">
                                <a href="{link}" target="_blank" class="news-title">{title}</a>
                                <div class="news-meta">
                                    <span class="source-badge">{source}</span>
                                    <span class="date-text">{date}</span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                except Exception as e:
                    st.error(f"Signal Interference: {str(e)}")

        # --- Tab 2: Instagram Search ---
        with tab2:
            st.markdown("<h4 style='text-align: center; color: #833ab4;'>📡 SCANNING BREU ENTERTAINMENT FEED</h4>", unsafe_allow_html=True)
            with st.spinner(f"Searching Label Archives for {artist_name}..."):
                params = {
                    "engine": "google",
                    "q": f"site:instagram.com/breuentertainment/ {artist_name}",
                    "api_key": api_key,
                    "num": 10
                }

                try:
                    search = GoogleSearch(params)
                    results = search.get_dict()
                    organic_results = results.get("organic_results", [])

                    st.markdown("<br>", unsafe_allow_html=True)

                    if not organic_results:
                        st.warning(f"No mentions of {artist_name} found on the Breu Entertainment feed.")
                        st.markdown(f"<div style='text-align: center; margin-top: 10px;'><a href='https://www.instagram.com/breuentertainment/' target='_blank' style='color: #d4af37;'>View Full Feed on Instagram ↗</a></div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<h3 style='text-align: center; margin-bottom: 30px;'>LABEL ARCHIVES ({len(organic_results)})</h3>", unsafe_allow_html=True)
                        
                        for result in organic_results:
                            title = result.get("title", "Instagram Post")
                            link = result.get("link", "#")
                            snippet = result.get("snippet", "")
                            
                            # Custom styling for IG cards
                            st.markdown(f"""
                            <div class="news-card" style="border-left: 3px solid #833ab4;">
                                <a href="{link}" target="_blank" class="news-title" style="color: #e1306c;">{title}</a>
                                <div class="news-meta" style="margin-top: 5px;">
                                    <span class="source-badge" style="background-color: #833ab4; color: white;">BREU ENTERTAINMENT</span>
                                </div>
                                <p style="color: #ccc; font-size: 0.9rem; margin-top: 10px;">{snippet}</p>
                            </div>
                            """, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Visual Link Failure: {str(e)}")

elif search_button and not artist_name:
    st.warning("Please enter an artist name to begin.")

# --- Footer ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #555; font-size: 0.8rem;'>© 2024 OLIVIER NEO-JAZZ RECORDS</div>", unsafe_allow_html=True)
