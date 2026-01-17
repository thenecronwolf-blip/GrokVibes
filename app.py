import streamlit as st
import random
import pandas as pd
from collections import Counter
import google.generativeai as genai # Assuming Gemini Key based on typical Streamlit usage

# ==============================
# 1. API & NEURAL CONFIG
# ==============================
st.set_page_config(page_title="GrokVibes // NEURAL PRISM", page_icon="💎", layout="wide")

# Fetch API Key from Secrets
API_KEY = st.secrets.get("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

if "favorites" not in st.session_state: st.session_state.favorites = []
if "search_input" not in st.session_state: st.session_state.search_input = ""
if "ai_results" not in st.session_state: st.session_state.ai_results = []

def set_search(val):
    st.session_state.search_input = val

# ==============================
# 2. THE MEGA-HYBRID VAULT (EXTENDED)
# ==============================
VAULT = [
    # --- MUSIC: NEW WEIRD/DARK ENTRIES ---
    {"n": "100 gecs", "cat": "Music", "v": ["weird", "hyperpop", "glitch", "aggressive", "fast", "chaotic"], "c": "#00FF00", "stats": [8, 2, 10, 3]},
    {"n": "Slowdive", "cat": "Music", "v": ["sad", "shoegaze", "dreamy", "ethereal", "slow", "chill"], "c": "#00CCFF", "stats": [1, 9, 7, 10]},
    {"n": "Cocteau Twins", "cat": "Music", "v": ["weird", "angelic", "dreamy", "80s", "ethereal", "vocal"], "c": "#FF99CC", "stats": [1, 5, 10, 9]},
    {"n": "$uicideboy$", "cat": "Music", "v": ["dark", "rap", "aggressive", "sad", "distorted", "phonk"], "c": "#333333", "stats": [9, 8, 6, 2]},
    {"n": "Night Lovell", "cat": "Music", "v": ["dark", "deep", "rap", "slow", "atmospheric", "vibe"], "c": "#111111", "stats": [6, 6, 8, 5]},
    {"n": "Scarlxrd", "cat": "Music", "v": ["aggressive", "metal", "rap", "trap-metal", "fast", "angry"], "c": "#FF0000", "stats": [10, 3, 7, 1]},
    
    # --- ANIME: NEW AESTHETIC ENTRIES ---
    {"n": "Paprika", "cat": "Anime", "v": ["weird", "surreal", "psychological", "dreamy", "colorful", "scary"], "c": "#FF3300", "stats": [4, 4, 10, 5]},
    {"n": "Mononoke (Series)", "cat": "Anime", "v": ["weird", "horror", "artistic", "japanese", "mystery", "slow"], "c": "#FFCC00", "stats": [3, 4, 10, 6]},
    {"n": "Gantz", "cat": "Anime", "v": ["aggressive", "dark", "scifi", "blood", "aliens", "tragedy"], "c": "#000000", "stats": [10, 8, 7, 1]},
    {"n": "Casshern Sins", "cat": "Anime", "v": ["sad", "depressing", "scifi", "action", "ruins", "atmospheric"], "c": "#CCCCCC", "stats": [6, 10, 7, 4]},
    {"n": "Ergo Proxy", "cat": "Anime", "v": ["weird", "dark", "goth", "scifi", "mystery", "slow", "philosophical"], "c": "#222222", "stats": [4, 7, 9, 4]},
    {"n": "Initial D", "cat": "Anime", "v": ["cars", "eurobeat", "90s", "action", "drift", "fast"], "c": "#FFFFFF", "stats": [7, 2, 4, 8]},
]
# ... (Previous Vault entries included automatically)

# ==============================
# 3. PRISM-X UI STYLING
# ==============================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&display=swap');
    
    [data-testid="stAppViewContainer"] {
        background: #000;
        color: #fff;
        font-family: -apple-system, sans-serif;
    }

    /* NEON GLOW TEXT */
    .neon-text {
        font-family: 'Syncopate', sans-serif;
        text-transform: uppercase;
        letter-spacing: 5px;
        color: #fff;
        text-shadow: 0 0 10px #FF0055, 0 0 20px #FF0055;
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* ANIMATED PRISM CARDS */
    .prism-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 24px;
        position: relative;
        overflow: hidden;
        transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .prism-card::before {
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
        transition: 0.5s;
    }

    .prism-card:hover::before { left: 100%; }
    
    .prism-card:hover {
        transform: scale(1.02) translateY(-10px);
        background: rgba(255, 255, 255, 0.07);
        border-color: #00FFCC;
        box-shadow: 0 20px 40px rgba(0,0,0,0.6), 0 0 20px rgba(0,255,204,0.2);
    }

    /* NEURO-SYNTHESIS PANEL */
    .ai-panel {
        background: linear-gradient(135deg, rgba(112,0,255,0.1), rgba(0,255,204,0.1));
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================
# 4. NEURO-SYNTHESIS LOGIC
# ==============================
def run_neuro_synthesis(user_query):
    if not API_KEY:
        return "API Key missing in Streamlit Secrets."
    
    prompt = f"""
    Acting as a curator for an aesthetic database called GrokVibes. 
    The user is looking for a vibe described as: '{user_query}'.
    Return 3 music artists and 2 animes that fit this EXACT vibe but are NOT in this list: {", ".join([i['n'] for i in VAULT])}.
    Format: Name | Category | Short Vibe Description. Be niche, weird, and accurate.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Neural Link Error: {e}"

# ==============================
# 5. HEADER & SEARCH
# ==============================
st.markdown('<div class="neon-text">GROKVIBES</div>', unsafe_allow_html=True)

query = st.text_input("", placeholder="Inject vibe parameters (e.g. 'sad weird rap')", value=st.session_state.search_input)

# --- VIBE ENGINE ---
def get_matches(user_query, data):
    if not user_query: return random.sample(data, 12)
    u_tags = set(user_query.lower().split())
    scored = []
    for item in data:
        item_tags = set(item['v'] + [item['n'].lower(), item['cat'].lower()])
        score = len(u_tags.intersection(item_tags))
        if score > 0: scored.append((score, item))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [x[1] for x in scored]

results = get_matches(query, VAULT)

# --- VIBE RADAR & AI PANEL ---
col_stats, col_ai = st.columns([1, 1.5])

with col_stats:
    st.write("### 🧭 Vibe Radar")
    if query and results:
        avg = [sum(r['stats'][i] for r in results[:5])/5 for i in range(4)]
        radar_df = pd.DataFrame(dict(r=avg, theta=['Aggro', 'Sad', 'Weird', 'Chill']))
        st.vega_lite_chart(radar_df, {
            'mark': {'type': 'area', 'fill': '#00FFCC', 'stroke': '#00FFCC'},
            'encoding': {
                'theta': {'field': 'theta', 'type': 'nominal'},
                'radius': {'field': 'r', 'type': 'quantitative', 'scale': {'domain': [0, 10]}}
            },
            'view': {'stroke': None},
        }, use_container_width=True)

with col_ai:
    st.write("### 🧠 Neuro-Synthesis")
    if st.button("Initialize Neural Link", use_container_width=True):
        if query:
            with st.spinner("Synthesizing new frequencies..."):
                st.session_state.ai_results = run_neuro_synthesis(query)
        else:
            st.error("Input query required for synthesis.")
    
    if st.session_state.ai_results:
        st.markdown(f'<div class="ai-panel">{st.session_state.ai_results}</div>', unsafe_allow_html=True)

# ==============================
# 6. RESULTS GRID
# ==============================
st.write("### 📡 Local Frequencies")
if results:
    cols = st.columns(3)
    for i, res in enumerate(results[:21]):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="prism-card" style="border-left: 4px solid {res['c']};">
                <div style="font-size: 10px; color: {res['c']}; font-weight: 800; letter-spacing: 2px;">{res['cat']}</div>
                <div style="font-size: 24px; font-weight: 800; margin: 10px 0;">{res['n']}</div>
                <div style="font-size: 11px; opacity: 0.5;">{' '.join(['#'+t for t in res['v']])}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Action Row
            a1, a2 = st.columns(2)
            with a1: st.markdown(f"[▶ Stream](https://www.youtube.com/results?search_query={res['n'].replace(' ', '+')})")
            with a2:
                if st.button("♡ Save", key=f"fav_{res['n']}_{i}"):
                    if res['n'] not in st.session_state.favorites:
                        st.session_state.favorites.append(res['n'])
                        st.toast(f"Archived {res['n']}")

# ==============================
# 7. SIDEBAR PRESETS
# ==============================
with st.sidebar:
    st.markdown("### 🧬 Filter Presets")
    presets = ["Sad Weird Rap", "Aggressive Dark Anime", "Hyperpop Glitch", "Shoegaze Chill", "90s Cyberpunk"]
    for p in presets:
        st.button(p, on_click=set_search, args=(p,), use_container_width=True)
    
    st.divider()
    st.markdown("### 🖤 My Archive")
    for f in st.session_state.favorites:
        st.write(f"• {f}")
    if st.button("Clear Archive"):
        st.session_state.favorites = []
        st.rerun()
