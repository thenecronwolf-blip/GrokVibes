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
# STYLES
# ==============================

st.markdown("""
<style>
body { background-color: #0b0f19; color: #e6e6ff; }
.card {
    background: rgba(20, 24, 45, 0.95);
    border-radius: 14px;
    padding: 14px;
    margin-bottom: 12px;
    box-shadow: 0 0 12px rgba(120,130,255,0.2);
}
.tag {
    display: inline-block;
    margin-right: 6px;
    opacity: 0.7;
    font-size: 0.75rem;
}
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, #6f7dff, transparent);
}
</style>
""", unsafe_allow_html=True)

# ==============================
# MASSIVE DATABASE
# ==============================

ANIME_DB = [
    {"title": "Cyberpunk: Edgerunners", "tags": ["cyberpunk", "dark", "sad"]},
    {"title": "Akira", "tags": ["cyberpunk", "dystopia"]},
    {"title": "Ghost in the Shell", "tags": ["cyberpunk", "philosophical"]},
    {"title": "Serial Experiments Lain", "tags": ["dark", "psychological"]},
    {"title": "Ergo Proxy", "tags": ["dark", "sad", "cyberpunk"]},
    {"title": "Texhnolyze", "tags": ["dark", "bleak"]},
    {"title": "Devilman Crybaby", "tags": ["dark", "emotional"]},
    {"title": "Psycho-Pass", "tags": ["cyberpunk", "thriller"]},
    {"title": "Neon Genesis Evangelion", "tags": ["sad", "psychological"]},
    {"title": "A Silent Voice", "tags": ["sad", "emotional"]},
    {"title": "Your Lie in April", "tags": ["sad", "romance"]},
    {"title": "Samurai Champloo", "tags": ["lofi", "chill"]},
    {"title": "Cowboy Bebop", "tags": ["chill", "space", "jazz"]},
    {"title": "Mushishi", "tags": ["calm", "atmospheric"]},
    {"title": "Made in Abyss", "tags": ["dark", "emotional"]},
    {"title": "Paranoia Agent", "tags": ["psychological", "dark"]},
]

MUSIC_DB = [
    {"artist": "Crystal Castles", "tags": ["cyberpunk", "dark"]},
    {"artist": "Perturbator", "tags": ["cyberpunk", "synthwave"]},
    {"artist": "Carpenter Brut", "tags": ["dark", "synthwave"]},
    {"artist": "Gesaffelstein", "tags": ["dark", "industrial"]},
    {"artist": "Nujabes", "tags": ["lofi", "chill"]},
    {"artist": "J Dilla", "tags": ["lofi", "jazzy"]},
    {"artist": "idealism", "tags": ["lofi", "sad"]},
    {"artist": "Joji", "tags": ["sad", "emotional"]},
    {"artist": "Juice WRLD (unreleased)", "tags": ["sad", "emotional"]},
    {"artist": "nothing,nowhere.", "tags": ["sad", "emo"]},
    {"artist": "The Kid LAROI", "tags": ["sad", "melodic"]},
    {"artist": "Bad Omens", "tags": ["dark", "metal"]},
    {"artist": "I Prevail", "tags": ["dark", "metal"]},
    {"artist": "Bring Me The Horizon", "tags": ["dark", "alt"]},
    {"artist": "Nine Inch Nails", "tags": ["industrial", "dark"]},
]

# ==============================
# VIBE ENGINE
# ==============================

def extract_tags(text):
    words = re.findall(r"\b[a-z]+\b", text.lower())
    return set(words)

def match_items(db, tags):
    scored = []
    for item in db:
        score = len(tags.intersection(item["tags"]))
        if score > 0:
            scored.append((score, item))
    scored.sort(reverse=True, key=lambda x: x[0])
    return [item for _, item in scored]

def generate_recs(user_input, intensity):
    tags = extract_tags(user_input)

    anime_matches = match_items(ANIME_DB, tags)
    music_matches = match_items(MUSIC_DB, tags)

    if not anime_matches:
        anime_matches = ANIME_DB[:]
    if not music_matches:
        music_matches = MUSIC_DB[:]

    random.shuffle(anime_matches)
    random.shuffle(music_matches)

    return (
        anime_matches[: 3 + intensity],
        music_matches[: 3 + intensity],
    )

# ==============================
# SESSION STATE
# ==============================

if "history" not in st.session_state:
    st.session_state.history = []

# ==============================
# UI
# ==============================

st.title("GrokVibes 🎧")
st.markdown("*Anime + Music • Database-driven • Zero APIs*")
st.markdown("<hr>", unsafe_allow_html=True)

intensity = st.slider("Vibe intensity", 0, 3, 1)

presets = {
    "🌃 Cyberpunk": "neon cyberpunk night",
    "💔 Sad": "sad lonely night",
    "🌿 Chill": "lofi calm vibes",
    "🖤 Dark": "dark emotional anime",
}

cols = st.columns(len(presets))
for col, (label, vibe) in zip(cols, presets.items()):
    if col.button(label):
        st.session_state.vibe = vibe

user_input = st.text_input(
    "Drop your vibe 👇",
    value=st.session_state.get("vibe", ""),
    placeholder="sad cyberpunk night drive"
)

if st.button("Get Recs 🚀"):
    if user_input.strip():
        st.session_state.history.insert(0, user_input)

        anime, music = generate_recs(user_input, intensity)

        st.markdown("## 📺 Anime")
        for a in anime:
            st.markdown(
                f"<div class='card'><b>{a['title']}</b><br>"
                f"{' '.join(f'<span class=tag>#{t}</span>' for t in a['tags'])}"
                f"</div>",
                unsafe_allow_html=True
            )

        st.markdown("## 🎧 Music")
        for m in music:
            query = m["artist"].replace(" ", "+")
            st.markdown(
                f"<div class='card'><b>{m['artist']}</b><br>"
                f"{' '.join(f'<span class=tag>#{t}</span>' for t in m['tags'])}<br>"
                f"<a href='https://www.youtube.com/results?search_query={query}' target='_blank'>YouTube</a> | "
                f"<a href='https://open.spotify.com/search/{query}' target='_blank'>Spotify</a>"
                f"</div>",
                unsafe_allow_html=True
            )
    else:
        st.warning("Give me a vibe to work with 😏")

if st.session_state.history:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 🕘 Recent Vibes")
    for h in st.session_state.history[:6]:
        if st.button(h):
            st.session_state.vibe = h

st.caption("Open-source • Local database • No APIs • Neon forever 🌃")
