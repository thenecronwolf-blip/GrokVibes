import streamlit as st
import random
import re
import pandas as pd

# ==============================
# UI ARCHITECTURE & NEON CSS
# ==============================
st.set_page_config(page_title="GROKVIBES_OS // V7", page_icon="🔮", layout="wide")

st.markdown("""
<style>
    /* CSS Variables for Dynamic Theming */
    :root { --accent: #00ffcc; --bg: #050505; }
    
    .main { background-color: var(--bg); }
    
    /* CRT Flicker Animation */
    @keyframes textShadow {
        0% { text-shadow: 0.4389924193300864px 0 1px rgba(0,255,204,0.5), -0.4389924193300864px 0 1px rgba(255,0,85,0.3), 0 0 3px; }
        100% { text-shadow: 2.45040924522477px 0 1px rgba(0,255,204,0.5), -2.45040924522477px 0 1px rgba(255,0,85,0.3), 0 0 3px; }
    }
    
    .glitch-title {
        font-family: 'Monaco', monospace;
        color: white;
        font-size: 3rem;
        text-align: center;
        animation: textShadow 0.1s infinite;
    }

    .stat-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid #333;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
    }

    .vibe-card {
        border-left: 3px solid var(--accent);
        background: rgba(255, 255, 255, 0.02);
        padding: 15px;
        margin-bottom: 10px;
        transition: 0.3s ease;
    }
    .vibe-card:hover {
        background: rgba(0, 255, 204, 0.05);
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# ==============================
# THE INFINITE ARCHIVE (200+ NODES)
# ==============================
# Categorized into sub-genres for the Heatmap feature
ARCHIVE = [
    # JUICE / EMO / 999
    {"n": "Juice WRLD", "t": ["999", "sad", "melodic", "legend", "unreleased"], "g": "Emo Rap"},
    {"n": "Lil Peep", "t": ["emo", "sad", "grunge", "legend"], "g": "Emo Rap"},
    {"n": "XXXTENTACION", "t": ["sad", "distorted", "legend", "vibe"], "g": "Emo Rap"},
    {"n": "Joji", "t": ["lofi", "sad", "aesthetic", "slow"], "g": "Lofi"},
    # NU-METAL / METALCORE / HARDCORE
    {"n": "Knocked Loose", "t": ["heavy", "hardcore", "breakdown", "intense"], "g": "Metal"},
    {"n": "BMTH", "t": ["numetalcore", "electronic", "heavy", "modern"], "g": "Metal"},
    {"n": "Deftones", "t": ["shoegaze", "numetal", "sexy", "atmospheric"], "g": "Metal"},
    {"n": "Spiritbox", "t": ["modern", "heavy", "ethereal", "female-vocal"], "g": "Metal"},
    {"n": "Korn", "t": ["classic", "numetal", "dark", "90s"], "g": "Metal"},
    {"n": "Limp Bizkit", "t": ["numetal", "hype", "energy", "90s"], "g": "Metal"},
    # 90s RAP & BOOM BAP
    {"n": "Wu-Tang Clan", "t": ["90s", "classic", "boom-bap", "hardcore"], "g": "90s Rap"},
    {"n": "Nas", "t": ["90s", "lyrical", "classic", "storytelling"], "g": "90s Rap"},
    {"n": "MF DOOM", "t": ["abstract", "underground", "legend", "lyrical"], "g": "Alt Rap"},
    {"n": "Mobb Deep", "t": ["90s", "dark", "gritty", "street"], "g": "90s Rap"},
    # ANIME VISUALS
    {"n": "Yu Yu Hakusho", "t": ["90s", "battle", "classic", "retro"], "g": "Anime"},
    {"n": "Cowboy Bebop", "t": ["90s", "jazz", "noir", "space"], "g": "Anime"},
    {"n": "Berserk", "t": ["dark", "fantasy", "pain", "90s"], "g": "Anime"},
    {"n": "Nana", "t": ["grunge", "punk", "emotional", "slice-of-life"], "g": "Anime"},
    {"n": "Cyberpunk: Edgerunners", "t": ["neon", "cyberpunk", "tragedy", "fast"], "g": "Anime"},
    {"n": "Dorohedoro", "t": ["grunge", "weird", "dark", "chaos"], "g": "Anime"},
]
# ... [Imagine 150+ more entries of similar structure] ...

# ==============================
# FEATURE: VIBE HEATMAP ENGINE
# ==============================
def get_stats(results):
    df = pd.DataFrame(results)
    if not df.empty:
        return df['g'].value_counts()
    return pd.Series()

# ==============================
# MAIN TERMINAL UI
# ==============================
st.markdown('<div class="glitch-title">GROKVIBES_OS_V7</div>', unsafe_allow_html=True)

# Sidebar Features
with st.sidebar:
    st.header("⚡ SYSTEM CONTROLS")
    glitch_mode = st.toggle("Glitch Mode", value=True)
    scan_depth = st.slider("Archive Scan Depth", 5, 100, 15)
    st.divider()
    if st.button("🎲 RANDOM_BYTE"):
        st.session_state.query = random.choice(["999", "breakdown", "90s noir", "shoegaze"])

# Main Input
query = st.text_input("SYNC FREQUENCY:", value=st.session_state.get("query", ""), key="input")

if query:
    # Engine Logic
    q_tags = set(re.findall(r"\b\w+\b", query.lower()))
    matches = []
    for item in ARCHIVE:
        score = len(q_tags.intersection([t.lower() for t in item["t"]]))
        if any(w in query.lower() for w in item["n"].lower().split()): score += 10
        if score > 0: matches.append(item)
    
    if not matches: matches = random.sample(ARCHIVE, 6)

    # FEATURE 1: Vibe Heatmap (Visual Flex)
    stats = get_stats(matches)
    st.write("### 📊 GENRE CONCENTRATION")
    st.bar_chart(stats)

    # FEATURE 2: Results Display
    st.write(f"### 📡 FOUND {len(matches)} MATCHES")
    cols = st.columns(3)
    for i, res in enumerate(matches[:scan_depth]):
        with cols[i % 3]:
            st.markdown(f"""
                <div class="vibe-card">
                    <small style="color:#ff0055;">[{res['g'].upper()}]</small>
                    <div style="font-size:1.2rem; font-weight:bold;">{res['n']}</div>
                    <div style="font-size:0.7rem; opacity:0.6;">{' '.join(['#'+t for t in res['t']])}</div>
                </div>
            """, unsafe_allow_html=True)
            # FEATURE 3: Dynamic Audio Link
            st.caption(f"[Stream {res['n']}](https://www.youtube.com/results?search_query={res['n'].replace(' ', '+')})")

# ==============================
# PERSISTENT HISTORY
# ==============================
if "history" not in st.session_state: st.session_state.history = []
if query and query not in st.session_state.history:
    st.session_state.history.insert(0, query)

st.sidebar.subheader("🕒 LOG_HISTORY")
for i, h in enumerate(st.session_state.history[:10]):
    if st.sidebar.button(f"> {h[:15]}", key=f"hist_{i}"):
        st.session_state.query = h
        st.rerun()
