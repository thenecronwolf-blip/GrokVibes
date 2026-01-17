import streamlit as st
import random
import re

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="GrokVibes 🎧",
    page_icon="🌃",
    layout="centered"
)

# ==============================
# ENHANCED STYLES (Glassmorphism)
# ==============================
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #e6e6ff;
    }
    .stButton>button {
        border-radius: 20px;
        transition: all 0.3s ease;
        border: 1px solid #6f7dff !important;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px #6f7dff;
    }
    .card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        transition: 0.3s;
    }
    .card:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: #6f7dff;
    }
    .tag {
        color: #00d4ff;
        font-weight: bold;
        margin-right: 8px;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# ==============================
# THE MEGA LIBRARY (Expanded)
# ==============================
ANIME_DB = [
    {"title": "Cyberpunk: Edgerunners", "tags": ["cyberpunk", "dark", "sad", "neon"]},
    {"title": "Akira", "tags": ["cyberpunk", "dystopia", "classic"]},
    {"title": "Ghost in the Shell", "tags": ["cyberpunk", "philosophical", "future"]},
    {"title": "Serial Experiments Lain", "tags": ["dark", "psychological", "glitch"]},
    {"title": "Ergo Proxy", "tags": ["dark", "sad", "cyberpunk", "mystery"]},
    {"title": "Texhnolyze", "tags": ["dark", "bleak", "industrial"]},
    {"title": "Devilman Crybaby", "tags": ["dark", "emotional", "intense"]},
    {"title": "Psycho-Pass", "tags": ["cyberpunk", "thriller", "dystopia"]},
    {"title": "Neon Genesis Evangelion", "tags": ["sad", "psychological", "mecha"]},
    {"title": "A Silent Voice", "tags": ["sad", "emotional", "slice of life"]},
    {"title": "Your Lie in April", "tags": ["sad", "romance", "music"]},
    {"title": "Samurai Champloo", "tags": ["lofi", "chill", "hiphop"]},
    {"title": "Cowboy Bebop", "tags": ["chill", "space", "jazz", "noir"]},
    {"title": "Mushishi", "tags": ["calm", "atmospheric", "nature"]},
    {"title": "Made in Abyss", "tags": ["dark", "emotional", "adventure"]},
    {"title": "March Comes in Like a Lion", "tags": ["sad", "calm", "healing"]},
    {"title": "Perfect Blue", "tags": ["dark", "psychological", "thriller"]},
    {"title": "Sonny Boy", "tags": ["weird", "philosophical", "artistic"]},
    {"title": "Vivy: Fluorite Eye's Song", "tags": ["cyberpunk", "music", "action"]}
]

MUSIC_DB = [
    {"artist": "Crystal Castles", "tags": ["cyberpunk", "dark", "glitch"]},
    {"artist": "Perturbator", "tags": ["cyberpunk", "synthwave", "dark"]},
    {"artist": "Carpenter Brut", "tags": ["dark", "synthwave", "action"]},
    {"artist": "Gesaffelstein", "tags": ["dark", "industrial", "techno"]},
    {"artist": "Nujabes", "tags": ["lofi", "chill", "jazzy"]},
    {"artist": "J Dilla", "tags": ["lofi", "jazzy", "beats"]},
    {"artist": "Slowdive", "tags": ["shoegaze", "dreamy", "calm"]},
    {"artist": "Beach House", "tags": ["dreamy", "sad", "chill"]},
    {"artist": "Joji", "tags": ["sad", "emotional", "lofi"]},
    {"artist": "Burial", "tags": ["ambient", "dark", "future", "rainy"]},
    {"artist": "Kordhell", "tags": ["phonk", "aggressive", "drift"]},
    {"artist": "Hensonn", "tags": ["phonk", "chill", "dark"]},
    {"artist": "Cocteau Twins", "tags": ["ethereal", "dreamy", "classic"]},
    {"artist": "Deftones", "tags": ["dark", "shoegaze", "intense"]},
    {"artist": "Lana Del Rey", "tags": ["sad", "cinematic", "vintage"]},
    {"artist": "Sewerslvt", "tags": ["breakcore", "dark", "sad", "glitch"]}
]

# ==============================
# LOGIC ENGINE
# ==============================
def extract_tags(text):
    return set(re.findall(r"\b[a-z]+\b", text.lower()))

def generate_recs(user_input, intensity):
    tags = extract_tags(user_input)
    
    def score_items(db):
        scored = []
        for item in db:
            match_count = len(tags.intersection(item["tags"]))
            if match_count > 0:
                scored.append(item)
        if not scored: return random.sample(db, min(len(db), 5))
        return scored

    anime = score_items(ANIME_DB)
    music = score_items(MUSIC_DB)
    
    random.shuffle(anime)
    random.shuffle(music)
    
    num_results = 3 + intensity
    return anime[:num_results], music[:num_results]

# ==============================
# UI RENDER
# ==============================
st.title("GrokVibes 🎧")
st.caption("v2.0 • The Ethereal Update")

# Intensity determines result count
intensity = st.sidebar.select_slider("Vibe Depth", options=[1, 2, 3, 4, 5], value=2)

presets = {
    "🌌 Neon": "cyberpunk glitch dark",
    "☁️ Ethereal": "dreamy shoegaze calm",
    "🏎️ Phonk": "aggressive phonk dark",
    "☕ Lofi": "lofi chill rainy",
    "🌑 Void": "dark sad psychological"
}

# Horizontal Preset Buttons
p_cols = st.columns(len(presets))
for i, (label, text) in enumerate(presets.items()):
    if p_cols[i].button(label):
        st.session_state.vibe = text

# Search Bar
user_input = st.text_input("What's the energy?", value=st.session_state.get("vibe", ""), placeholder="e.g. rainy night in tokyo")

if st.button("Sync Vibe ⚡", use_container_width=True):
    if user_input:
        if "history" not in st.session_state: st.session_state.history = []
        if user_input not in st.session_state.history:
            st.session_state.history.insert(0, user_input)
        
        anime_res, music_res = generate_recs(user_input, intensity)

        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📺 Visuals")
            for a in anime_res:
                tags_html = "".join([f"<span class='tag'>#{t}</span>" for t in a['tags']])
                st.markdown(f"<div class='card'><b>{a['title']}</b><br>{tags_html}</div>", unsafe_allow_html=True)
        
        with col2:
            st.subheader("🎵 Audio")
            for m in music_res:
                tags_html = "".join([f"<span class='tag'>#{t}</span>" for t in m['tags']])
                st.markdown(
                    f"<div class='card'><b>{m['artist']}</b><br>{tags_html}<br>"
                    f"<small><a href='https://music.youtube.com/search?q={m['artist']}' style='color:#ff4b4b'>Listen Now</a></small></div>", 
                    unsafe_allow_html=True
                )
    else:
        st.info("Input a vibe or select a preset above.")

# Fixed History Loop
if "history" in st.session_state and st.session_state.history:
    st.divider()
    st.write("🕒 Previous States")
    # Using columns to make history look cleaner
    h_cols = st.columns(4)
    for i, h in enumerate(st.session_state.history[:8]):
        # KEY=f"hist_{i}" is the crucial fix for DuplicateElementId
        if h_cols[i % 4].button(h[:15], key=f"hist_{i}", help=h):
            st.session_state.vibe = h
            st.rerun()
