import streamlit as st
import random
import re

# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="GrokVibes 🎧",
    page_icon="🎧",
    layout="centered"
)

# ==============================
# CYBERPUNK CSS
# ==============================

st.markdown("""
<style>
body {
    background-color: #0b0f19;
    color: #e0e0ff;
}
.card {
    background: rgba(20, 24, 45, 0.9);
    border-radius: 14px;
    padding: 14px;
    margin-bottom: 12px;
    box-shadow: 0 0 12px rgba(100,120,255,0.15);
}
.small {
    opacity: 0.7;
    font-size: 0.85rem;
}
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, #6f7dff, transparent);
}
</style>
""", unsafe_allow_html=True)

# ==============================
# LOCAL DATABASE
# ==============================

DB = {
    "cyberpunk": {
        "keywords": ["cyber", "neon", "dystopia", "future", "tech"],
        "anime": [
            "Cyberpunk: Edgerunners — neon chaos & tragedy",
            "Ghost in the Shell — cyber philosophy",
            "Akira — raw dystopian power",
            "Psycho-Pass — tech morality",
        ],
        "music": [
            "Crystal Castles",
            "Perturbator",
            "Carpenter Brut",
            "Gesaffelstein",
        ],
    },
    "lofi": {
        "keywords": ["lofi", "chill", "study", "calm"],
        "anime": [
            "Samurai Champloo — chill hip-hop soul",
            "Mushishi — peaceful atmosphere",
            "Kids on the Slope — late-night jazz",
        ],
        "music": [
            "Nujabes",
            "idealism",
            "Tomppabeats",
            "J Dilla",
        ],
    },
    "sad": {
        "keywords": ["sad", "lonely", "heart", "cry", "night"],
        "anime": [
            "Your Lie in April — emotional devastation",
            "A Silent Voice — quiet pain",
            "Ergo Proxy — isolation & dread",
        ],
        "music": [
            "Juice WRLD (unreleased)",
            "Joji",
            "nothing,nowhere.",
            "The Kid LAROI",
        ],
    },
    "dark": {
        "keywords": ["dark", "heavy", "anger", "rage"],
        "anime": [
            "Devilman Crybaby — emotional destruction",
            "Serial Experiments Lain — existential spiral",
            "Texhnolyze — hopeless cyber decay",
        ],
        "music": [
            "Bad Omens",
            "I Prevail",
            "Bring Me The Horizon",
            "Nine Inch Nails",
        ],
    },
}

# ==============================
# VIBE ENGINE
# ==============================

def detect_vibes(text):
    text = text.lower()
    scores = {}

    for vibe, data in DB.items():
        score = 0
        for kw in data["keywords"]:
            if re.search(rf"\b{kw}\b", text):
                score += 1
        if score:
            scores[vibe] = score

    if not scores:
        return list(DB.keys())

    return sorted(scores, key=scores.get, reverse=True)

def generate_recs(user_input, intensity):
    vibes = detect_vibes(user_input)
    anime, music = [], []

    for v in vibes:
        anime.extend(DB[v]["anime"])
        music.extend(DB[v]["music"])

    random.shuffle(anime)
    random.shuffle(music)

    anime = anime[: 3 + intensity]
    music = music[: 3 + intensity]

    return anime, music

# ==============================
# SESSION STATE
# ==============================

if "history" not in st.session_state:
    st.session_state.history = []

# ==============================
# UI HEADER
# ==============================

st.title("GrokVibes 🎧")
st.markdown("*Anime + Music Vibes • No APIs • Built by @JoeyxHerrmann*")
st.markdown("<hr>", unsafe_allow_html=True)

# ==============================
# CONTROLS
# ==============================

intensity = st.slider("Vibe intensity", 0, 2, 1)

presets = {
    "🌃 Cyberpunk": "neon cyberpunk night",
    "💔 Sad": "sad night drive",
    "🌿 Lo-Fi": "lofi chill study",
    "🖤 Dark": "dark anime rage",
}

cols = st.columns(len(presets))
for col, (label, text) in zip(cols, presets.items()):
    if col.button(label):
        st.session_state.vibe = text

user_input = st.text_input(
    "Drop your vibe 👇",
    value=st.session_state.get("vibe", ""),
    placeholder="sad cyberpunk night 🌃"
)

# ==============================
# GENERATE
# ==============================

if st.button("Get Recs 🚀"):
    if user_input.strip():
        st.session_state.history.insert(0, user_input)

        anime, music = generate_recs(user_input, intensity)

        st.markdown("## 📺 Anime Picks")
        for a in anime:
            st.markdown(f"<div class='card'>{a}</div>", unsafe_allow_html=True)

        st.markdown("## 🎧 Music Picks")
        for m in music:
            st.markdown(
                f"<div class='card'>{m}<br>"
                f"<span class='small'>🔎 <a href='https://www.youtube.com/results?search_query={m.replace(' ', '+')}' target='_blank'>YouTube</a> | "
                f"<a href='https://open.spotify.com/search/{m.replace(' ', '%20')}' target='_blank'>Spotify</a></span></div>",
                unsafe_allow_html=True
            )

    else:
        st.warning("Give me *something* to feel 😏")

# ==============================
# HISTORY
# ==============================

if st.session_state.history:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 🕘 Recent Vibes")
    for h in st.session_state.history[:5]:
        if st.button(h):
            st.session_state.vibe = h

# ==============================
# FOOTER
# ==============================

st.caption("Open-source • GitHub-safe • Zero APIs • Neon nights only 🌃")
