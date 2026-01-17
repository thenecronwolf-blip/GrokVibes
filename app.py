import streamlit as st
import random
import re

# ==============================
# 1. PAGE CONFIG & SYSTEM STATE
# ==============================
st.set_page_config(page_title="GrokVibes", page_icon="🎧", layout="wide")

# State Initialization
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "ios_search" not in st.session_state:
    st.session_state.ios_search = ""

# Callback for UI Micro-interactions (Fixes the crash)
def set_search(mood_name):
    st.session_state.ios_search = mood_name

# ==============================
# 2. iOS 26 VISUAL ARCHITECTURE
# ==============================
st.markdown("""
<style>
    /* iOS 26 Acrylic Backdrop */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 0% 0%, #1a1a1a 0%, #000 100%);
        color: #FFFFFF;
    }

    /* Volumetric Glass Cards */
    .ios-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(25px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 28px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        transition: transform 0.4s cubic-bezier(0.15, 0.83, 0.66, 1);
    }
    
    .ios-card:hover {
        transform: scale(1.02);
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* Dynamic Island Input Styling */
    .stTextInput>div>div>input {
        background: rgba(255, 255, 255, 0.07) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 40px !important;
        color: white !important;
        padding: 15px 30px !important;
        font-size: 1.1rem !important;
    }

    .title-text {
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 800;
        font-size: 52px;
        letter-spacing: -2px;
        background: linear-gradient(180deg, #fff 0%, #888 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 30px;
    }

    .pill {
        background: rgba(255, 255, 255, 0.1);
        color: rgba(255, 255, 255, 0.9);
        padding: 5px 15px;
        border-radius: 100px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 8px;
        border: 1px solid rgba(255,255,255,0.05);
    }
</style>
""", unsafe_allow_html=True)

# ==============================
# 3. THE EXPANDED ARCHIVE (300+ SIMULATED)
# ==============================
VAULT = [
    {"n": "Juice WRLD", "m": "Heartbreak", "t": ["999", "melodic", "legend"], "cat": "Music"},
    {"n": "The Kid LAROI", "m": "Heartbreak", "t": ["melodic", "999", "pop-rap"], "cat": "Music"},
    {"n": "Lil Peep", "m": "Sad", "t": ["emo", "grunge", "legend"], "cat": "Music"},
    {"n": "Knocked Loose", "m": "Aggressive", "t": ["hardcore", "heavy", "breakdown"], "cat": "Music"},
    {"n": "Bring Me The Horizon", "m": "Aggressive", "t": ["modern", "nu-metalcore", "electronic"], "cat": "Music"},
    {"n": "Deftones", "m": "Dreamy", "t": ["shoegaze", "sexy", "atmospheric"], "cat": "Music"},
    {"n": "Joji", "m": "Dreamy", "t": ["lofi", "sad", "aesthetic"], "cat": "Music"},
    {"n": "Crystal Castles", "m": "Neon", "t": ["glitch", "cyberpunk", "electronic"], "cat": "Music"},
    {"n": "MF DOOM", "m": "Lyrical", "t": ["abstract", "underground", "legend"], "cat": "Music"},
    {"n": "Nana", "m": "Sad", "t": ["90s", "grunge", "emotional"], "cat": "Anime"},
    {"n": "Chainsaw Man", "m": "Aggressive", "t": ["chaos", "intense", "modern"], "cat": "Anime"},
    {"n": "Cowboy Bebop", "m": "Dreamy", "t": ["jazz", "space", "noir"], "cat": "Anime"},
    {"n": "Cyberpunk: Edgerunners", "m": "Neon", "t": ["cyberpunk", "tragedy", "fast"], "cat": "Anime"}
]

# Generators to fill the library
for i in range(250):
    VAULT.append({
        "n": f"Artist {100+i}", 
        "m": random.choice(["Sad", "Dark", "Neon", "Aggressive", "Lyrical"]), 
        "t": ["discovery", "vault"], 
        "cat": "Discover"
    })

# ==============================
# 4. DISCOVERY INTERFACE
# ==============================
st.markdown('<div class="title-text">Discovery</div>', unsafe_allow_html=True)

# Dynamic Island Search Bar
search_val = st.text_input("", placeholder="Search artists, moods, or genres...", key="ios_search")

# Mood Bubbles
st.write("### Choose a Mood")
mood_cols = st.columns(6)
mood_options = ["Heartbreak", "Aggressive", "Dreamy", "Lyrical", "Dark", "Neon"]

for i, mood in enumerate(mood_options):
    mood_cols[i].button(mood, key=f"btn_{mood}", on_click=set_search, args=(mood,))

# ==============================
# 5. RESULTS GRID & FAVORITES
# ==============================
if search_val:
    q = search_val.lower()
    results = [item for item in VAULT if q in item['n'].lower() or q in item['m'].lower() or any(q in t for t in item['t'])]
    
    if results:
        col1, col2 = st.columns(2)
        for i, item in enumerate(results[:24]):
            with (col1 if i % 2 == 0 else col2):
                tags_html = "".join([f"<span class='pill'>{t}</span>" for t in item['t']])
                
                # The Acrylic Card
                st.markdown(f"""
                    <div class="ios-card">
                        <div style="font-size: 11px; font-weight: 800; color: #ff3b30; text-transform: uppercase; margin-bottom: 4px;">{item['cat']} • {item['m']}</div>
                        <div style="font-size: 22px; font-weight: 700; margin-bottom: 12px;">{item['n']}</div>
                        {tags_html}
                    </div>
                """, unsafe_allow_html=True)
                
                # Card Actions
                act1, act2 = st.columns([1, 1])
                with act1:
                    st.markdown(f"<a href='https://www.youtube.com/results?search_query={item['n']}' style='color:#007aff; text-decoration:none; font-size:14px; font-weight:600;'>Listen Now ›</a>", unsafe_allow_html=True)
                with act2:
                    if st.button(f"❤️ Favorite", key=f"fav_{item['n']}_{i}"):
                        if item['n'] not in st.session_state.favorites:
                            st.session_state.favorites.append(item['n'])
                            st.toast(f"Added {item['n']} to Library", icon="✅")
    else:
        st.info("No nodes found in the current frequency.")

# ==============================
# 6. SIDEBAR LIBRARY
# ==============================
with st.sidebar:
    st.markdown("## ❤️ Your Library")
    if not st.session_state.favorites:
        st.caption("No favorites saved yet.")
    for fav in st.session_state.favorites:
        st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); padding: 12px; border-radius: 18px; margin-bottom: 8px; border: 1px solid rgba(255,255,255,0.1);">
                <span style="font-size: 14px; font-weight: 600;">{fav}</span>
            </div>
        """, unsafe_allow_html=True)
    
    if st.button("Clear Library"):
        st.session_state.favorites = []
        st.rerun()
