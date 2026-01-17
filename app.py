import streamlit as st
import random
import re

# ==============================
# 1. PAGE SETUP & DYNAMIC STATE
# ==============================
st.set_page_config(page_title="GrokVibes // NEON", page_icon="🔮", layout="wide")

if "favorites" not in st.session_state: st.session_state.favorites = []
if "search_query" not in st.session_state: st.session_state.search_query = ""

def set_search(val):
    st.session_state.search_query = val

# ==============================
# 2. CYBER-NEON GRAPHICS (iOS 26 Style)
# ==============================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    [data-testid="stAppViewContainer"] {
        background: #020205;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }

    /* Neon Pulse Animations */
    @keyframes glow {
        0% { box-shadow: 0 0 5px #ff0055; }
        50% { box-shadow: 0 0 20px #ff0055; }
        100% { box-shadow: 0 0 5px #ff0055; }
    }

    .neon-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .neon-card:hover {
        transform: translateY(-10px);
        border: 1px solid #00ffcc;
        box-shadow: 0 10px 30px rgba(0, 255, 204, 0.2);
    }

    .stTextInput>div>div>input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid #333 !important;
        border-radius: 15px !important;
        color: #00ffcc !important;
        font-weight: bold !important;
    }

    .pill-999 { background: #ff0055; color: white; padding: 2px 10px; border-radius: 10px; font-size: 10px; font-weight: bold; }
    .pill-heavy { background: #7000ff; color: white; padding: 2px 10px; border-radius: 10px; font-size: 10px; font-weight: bold; }
    .pill-retro { background: #00d4ff; color: white; padding: 2px 10px; border-radius: 10px; font-size: 10px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ==============================
# 3. THE HAND-CURATED VAULT (No Fillers)
# ==============================
VAULT = [
    # --- JUICE WRLD / 999 / EMO ---
    {"n": "Juice WRLD", "m": "Sad", "t": ["999", "legend", "melodic"], "style": "pill-999"},
    {"n": "Lil Peep", "m": "Sad", "t": ["emo", "grunge", "legend"], "style": "pill-999"},
    {"n": "XXXTENTACION", "m": "Sad", "t": ["distorted", "vibe", "legend"], "style": "pill-999"},
    {"n": "The Kid LAROI", "m": "Chill", "t": ["999", "pop-rap", "melodic"], "style": "pill-999"},
    {"n": "Joji", "m": "Chill", "t": ["lofi", "aesthetic", "slow"], "style": "pill-999"},
    {"n": "Polo G", "m": "Lyrical", "t": ["street", "melodic", "chicago"], "style": "pill-999"},
    
    # --- NU-METALCORE / HEAVY ---
    {"n": "Knocked Loose", "m": "Aggressive", "t": ["hardcore", "heavy", "breakdown"], "style": "pill-heavy"},
    {"n": "BMTH", "m": "Aggressive", "t": ["metalcore", "modern", "hybrid"], "style": "pill-heavy"},
    {"n": "Bad Omens", "m": "Dark", "t": ["intense", "melodic", "modern"], "style": "pill-heavy"},
    {"n": "Deftones", "m": "Dreamy", "t": ["shoegaze", "sexy", "atmospheric"], "style": "pill-heavy"},
    {"n": "Sleep Token", "m": "Dark", "t": ["atmospheric", "mystery", "heavy"], "style": "pill-heavy"},
    {"n": "Spiritbox", "m": "Dark", "t": ["metalcore", "ethereal", "modern"], "style": "pill-heavy"},
    {"n": "Korn", "m": "Aggressive", "t": ["numetal", "90s", "classic"], "style": "pill-heavy"},
    {"n": "Loathe", "m": "Dreamy", "t": ["shoegaze", "heavy", "experimental"], "style": "pill-heavy"},
    
    # --- 90s BOOM BAP / ALT RAP ---
    {"n": "Wu-Tang Clan", "m": "Lyrical", "t": ["90s", "classic", "hardcore"], "style": "pill-retro"},
    {"n": "MF DOOM", "m": "Lyrical", "t": ["alternative", "abstract", "legend"], "style": "pill-retro"},
    {"n": "Nas", "m": "Lyrical", "t": ["90s", "storytelling", "classic"], "style": "pill-retro"},
    {"n": "Mobb Deep", "m": "Dark", "t": ["90s", "gritty", "street"], "style": "pill-retro"},
    {"n": "Tyler, The Creator", "m": "Chill", "t": ["alternative", "weird", "art"], "style": "pill-retro"},
    {"n": "Earl Sweatshirt", "m": "Dark", "t": ["abstract", "depressing", "alternative"], "style": "pill-retro"},

    # --- PHONK / GLITCH ---
    {"n": "Crystal Castles", "m": "Dark", "t": ["glitch", "cyberpunk", "chaos"], "style": "pill-retro"},
    {"n": "Kordhell", "m": "Aggressive", "t": ["phonk", "drift", "fast"], "style": "pill-retro"},
    {"n": "Hensonn", "m": "Chill", "t": ["phonk", "dark", "smooth"], "style": "pill-retro"},

    # --- ANIME VISUALS ---
    {"n": "Chainsaw Man", "m": "Aggressive", "t": ["chaos", "intense", "modern"], "style": "pill-heavy"},
    {"n": "Nana", "m": "Sad", "t": ["grunge", "punk", "90s"], "style": "pill-999"},
    {"n": "Cowboy Bebop", "m": "Chill", "t": ["90s", "jazz", "space"], "style": "pill-retro"},
    {"n": "Cyberpunk: Edgerunners", "m": "Neon", "t": ["tragedy", "fast", "glitch"], "style": "pill-retro"},
    {"n": "Yu Yu Hakusho", "m": "Classic", "t": ["90s", "battle", "shonen"], "style": "pill-retro"},
    {"n": "Tokyo Ghoul", "m": "Dark", "t": ["tragedy", "numetal", "ghoul"], "style": "pill-heavy"},
    {"n": "Berserk (1997)", "m": "Dark", "t": ["pain", "90s", "dark-fantasy"], "style": "pill-heavy"},
]

# ==============================
# 4. NEON-FLEX UI LOGIC
# ==============================
st.markdown('<h1 style="text-align:center; color:#00ffcc; text-shadow: 0 0 10px #00ffcc;">GROKVIBES DISCOVERY</h1>', unsafe_allow_html=True)

# Mood Bubbles
mood_cols = st.columns(6)
moods = ["Sad", "Aggressive", "Chill", "Lyrical", "Dark", "Neon"]
for i, m in enumerate(moods):
    mood_cols[i].button(m, key=f"m_{i}", on_click=set_search, args=(m,), use_container_width=True)

# Search Input
query = st.text_input("Search the Vault", value=st.session_state.search_query, key="vault_search", placeholder="Type a name, genre, or vibe...")

# Display Results
if query or st.session_state.search_query:
    q = (query if query else st.session_state.search_query).lower()
    matches = [i for i in VAULT if q in i['n'].lower() or q in i['m'].lower() or any(q in t for t in i['t'])]
    
    if matches:
        cols = st.columns(3)
        for idx, item in enumerate(matches):
            with cols[idx % 3]:
                st.markdown(f"""
                    <div class="neon-card">
                        <span class="{item['style']}">{item['m'].upper()}</span>
                        <div style="font-size:24px; font-weight:900; margin-top:10px; color:white;">{item['n']}</div>
                        <div style="margin-top:10px;">{' '.join([f'<span style="color:#666; font-size:12px; margin-right:8px;">#{t}</span>' for t in item['t']])}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Action Buttons
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    st.markdown(f"[▶ Stream](https://www.youtube.com/results?search_query={item['n'].replace(' ', '+')})")
                with btn_col2:
                    if st.button(f"♡ Save", key=f"fav_{idx}"):
                        if item['n'] not in st.session_state.favorites:
                            st.session_state.favorites.append(item['n'])
                            st.toast(f"Saved {item['n']} to Library")
    else:
        st.warning("No matches in the current frequency. Try '999' or 'Hardcore'.")
else:
    # Home View
    st.markdown("### 🔥 Trending in the Vault")
    home_cols = st.columns(4)
    for i, item in enumerate(random.sample(VAULT, 4)):
        with home_cols[i]:
            st.markdown(f'<div class="neon-card"><div style="font-weight:bold;">{item["n"]}</div></div>', unsafe_allow_html=True)

# ==============================
# 5. SIDEBAR LIBRARY (Acrylic)
# ==============================
with st.sidebar:
    st.markdown("## 💜 YOUR LIBRARY")
    if not st.session_state.favorites:
        st.caption("Library empty. Save some vibes.")
    for f in st.session_state.favorites:
        st.markdown(f"""<div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:10px; margin-bottom:5px;">{f}</div>""", unsafe_allow_html=True)
    if st.button("Clear Archive"):
        st.session_state.favorites = []
        st.rerun()
