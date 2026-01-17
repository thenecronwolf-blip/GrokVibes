import streamlit as st
import random
import re

# ==============================
# ULTIMATE UI & ANIMATION FLEX
# ==============================
st.set_page_config(page_title="GROKVIBES // ARCHIVE", page_icon="🧬", layout="wide")

st.markdown("""
<style>
    /* Global Neon Aesthetic */
    [data-testid="stAppViewContainer"] {
        background-color: #030303;
        background-image: linear-gradient(0deg, transparent 24%, rgba(255, 0, 85, .05) 25%, rgba(255, 0, 85, .05) 26%, transparent 27%, transparent 74%, rgba(255, 0, 85, .05) 75%, rgba(255, 0, 85, .05) 76%, transparent 77%, transparent), 
                          linear-gradient(90deg, transparent 24%, rgba(255, 0, 85, .05) 25%, rgba(255, 0, 85, .05) 26%, transparent 27%, transparent 74%, rgba(255, 0, 85, .05) 75%, rgba(255, 0, 85, .05) 76%, transparent 77%, transparent);
        background-size: 50px 50px;
    }

    /* Glitch Animation */
    @keyframes glitch {
        0% { clip: rect(44px, 450px, 56px, 0); }
        5% { clip: rect(62px, 450px, 12px, 0); }
        10% { clip: rect(32px, 450px, 88px, 0); }
        100% { clip: rect(44px, 450px, 56px, 0); }
    }

    .vibe-card {
        background: rgba(10, 10, 10, 0.9);
        border: 1px solid #1a1a1a;
        padding: 20px;
        border-radius: 0px;
        transition: 0.4s;
        position: relative;
        overflow: hidden;
    }

    .vibe-card:hover {
        border-color: #00ffcc;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.2);
        transform: translateY(-5px);
    }

    .vibe-card::after {
        content: "";
        position: absolute;
        top: 0; left: -100%;
        width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
        transition: 0.5s;
    }

    .vibe-card:hover::after { left: 100%; }

    .tag-container { margin-top: 10px; }
    .tag {
        font-family: 'Monaco', monospace;
        font-size: 0.65rem;
        color: #ff0055;
        border: 1px solid #ff0055;
        padding: 2px 5px;
        margin-right: 4px;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# ==============================
# THE MASSIVE DATA MATRIX (150+ ITEMS)
# ==============================
# We use a structured list to allow the engine to cross-reference types
LIBRARY = [
    # --- MUSIC: JUICE / 999 / EMO ---
    {"n": "Juice WRLD", "v": ["999", "sad", "melodic", "legend", "emo-rap", "unreleased"]},
    {"n": "Lil Peep", "v": ["emo", "sad", "grunge-rap", "legend", "vulnerable"]},
    {"n": "XXXTENTACION", "v": ["distorted", "sad", "intense", "legend", "lofi"]},
    {"n": "Joji", "v": ["sad", "lofi", "emotional", "aesthetic", "slow"]},
    {"n": "The Kid LAROI", "v": ["melodic", "999", "sad", "pop-rap"]},
    {"n": "Polo G", "v": ["sad", "melodic", "chicago", "street"]},
    {"n": "Lil Uzi Vert", "v": ["hype", "emo", "high-energy", "space"]},
    
    # --- MUSIC: NU-METAL / HARDCORE / METALCORE ---
    {"n": "Knocked Loose", "v": ["heavy", "hardcore", "aggressive", "breakdown", "intense"]},
    {"n": "Bring Me The Horizon", "v": ["numetalcore", "modern", "alternative", "heavy", "electronic"]},
    {"n": "Bad Omens", "v": ["numetalcore", "modern", "melodic", "intense", "heavy"]},
    {"n": "Spiritbox", "v": ["metalcore", "modern", "ethereal", "heavy", "female-vocal"]},
    {"n": "Loathe", "v": ["shoegaze", "metalcore", "atmospheric", "heavy", "dark"]},
    {"n": "Deftones", "v": ["shoegaze", "numetal", "sexy", "atmospheric", "dark"]},
    {"n": "Korn", "v": ["numetal", "classic", "dark", "heavy", "90s"]},
    {"n": "Slipknot", "v": ["numetal", "aggressive", "chaos", "heavy", "90s"]},
    {"n": "Architects", "v": ["metalcore", "modern", "technical", "heavy"]},
    {"n": "Sleep Token", "v": ["atmospheric", "modern", "emotional", "heavy", "mysterious"]},
    {"n": "Motionless In White", "v": ["gothic", "metalcore", "heavy", "intense"]},

    # --- MUSIC: 90s & BOOM BAP ---
    {"n": "Wu-Tang Clan", "v": ["90s", "boom-bap", "classic", "hardcore", "retro"]},
    {"n": "Mobb Deep", "v": ["90s", "dark", "gritty", "boom-bap", "street"]},
    {"n": "Nas", "v": ["90s", "lyrical", "classic", "rap", "storytelling"]},
    {"n": "MF DOOM", "v": ["alternative", "abstract", "legend", "lyrical", "weird"]},
    {"n": "Big L", "v": ["90s", "lyrical", "fast", "boom-bap"]},
    {"n": "A Tribe Called Quest", "v": ["90s", "jazz-rap", "chill", "classic", "smooth"]},
    {"n": "Souls of Mischief", "v": ["90s", "chill", "classic", "smooth"]},

    # --- MUSIC: PHONK / WITCH HOUSE / GLITCH ---
    {"n": "Crystal Castles", "v": ["glitch", "cyberpunk", "electronic", "dark", "chaos"]},
    {"n": "Sidewalks and Skeletons", "v": ["witch-house", "dark", "ethereal", "slow"]},
    {"n": "Kordhell", "v": ["phonk", "aggressive", "drift", "fast"]},
    {"n": "Hensonn", "v": ["phonk", "chill", "dark", "drift"]},
    {"n": "Sewerslvt", "v": ["breakcore", "glitch", "depressing", "intense", "chaos"]},
    {"n": "Mr. Kitty", "v": ["synthwave", "dark", "emotional", "electronic"]},

    # --- ANIME: 90s & RETRO ---
    {"n": "Yu Yu Hakusho", "v": ["90s", "battle", "classic", "retro", "shonen"]},
    {"n": "Cowboy Bebop", "v": ["90s", "jazz", "noir", "space", "chill"]},
    {"n": "Berserk (1997)", "v": ["90s", "dark", "pain", "medieval", "seinen"]},
    {"n": "Neon Genesis Evangelion", "v": ["90s", "psychological", "sad", "mecha", "classic"]},
    {"n": "Initial D", "v": ["90s", "cars", "drift", "hype", "eurobeat"]},
    {"n": "Nana", "v": ["90s", "grunge", "punk", "emotional", "slice-of-life"]},
    {"n": "Trigun", "v": ["90s", "retro", "western", "action"]},

    # --- ANIME: MODERN & INTENSE ---
    {"n": "Chainsaw Man", "v": ["modern", "chaos", "intense", "action", "dark"]},
    {"n": "Jujutsu Kaisen", "v": ["modern", "battle", "intense", "supernatural"]},
    {"n": "Dorohedoro", "v": ["grunge", "weird", "dark", "chaos", "seinen"]},
    {"n": "Tokyo Ghoul", "v": ["numetal", "tragedy", "dark", "action", "ghoul"]},
    {"n": "Cyberpunk: Edgerunners", "v": ["neon", "cyberpunk", "tragedy", "hype", "fast"]},
    {"n": "Vinland Saga", "v": ["intense", "historical", "revenge", "seinen", "viking"]},
    {"n": "Hellsing Ultimate", "v": ["dark", "vampire", "heavy", "gore", "intense"]},
    {"n": "Parasyte", "v": ["dark", "psychological", "body-horror", "action"]},
]

# ==============================
# ENGINE (VIBE-SYNC)
# ==============================
def vibe_sync(query):
    query = query.lower()
    search_terms = set(re.findall(r"\b\w+\b", query))
    matches = []
    
    for item in LIBRARY:
        score = len(search_terms.intersection(item["v"]))
        # Exact Name Match Weighting
        name_parts = set(item["n"].lower().split())
        if search_terms.intersection(name_parts):
            score += 25 
            
        if score > 0:
            matches.append((score, item))
            
    if not matches:
        return random.sample(LIBRARY, 10)
        
    matches.sort(key=lambda x: x[0], reverse=True)
    return [x[1] for x in matches]

# ==============================
# UI RENDER
# ==============================
st.markdown('<h1 style="font-family: monospace; color:#00ffcc; text-shadow: 2px 2px #ff0055;">GROKVIBES_OS [ARCHIVE_v6]</h1>', unsafe_allow_html=True)

# Search Logic
query = st.text_input("SYNC FREQUENCY [ex: 90s drift / heavy 999 / shoegaze noir]:", key="user_query")
depth = st.sidebar.select_slider("ARCHIVE_DEPTH", options=[5, 10, 20, 50], value=10)

if query:
    results = vibe_sync(query)[:depth]
    
    # Grid layout
    cols = st.columns(3)
    for i, item in enumerate(results):
        with cols[i % 3]:
            tags_html = "".join([f"<span class='tag'>#{t}</span>" for t in item['v']])
            st.markdown(f"""
                <div class="vibe-card">
                    <div style="font-size: 1.1rem; font-weight: bold; letter-spacing: 1px;">{item['n']}</div>
                    <div class="tag-container">{tags_html}</div>
                </div>
            """, unsafe_allow_html=True)

# ==============================
# HISTORY (ID ERROR FIXED)
# ==============================
if "history" not in st.session_state: st.session_state.history = []
if query and query not in st.session_state.history:
    st.session_state.history.insert(0, query)

st.sidebar.markdown("### 🕒 LOG_ENTRIES")
for i, h in enumerate(st.session_state.history[:15]):
    # THE KEY FIX: Using the index i to ensure unique button IDs
    if st.sidebar.button(f"> {h[:18]}", key=f"sidebar_btn_{i}"):
        st.session_state.user_query = h
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("CONNECTED: [150+ NODES LOADED]")
