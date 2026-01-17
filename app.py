import streamlit as st
import random

# ==============================
# 1. APP CONFIGURATION
# ==============================
st.set_page_config(
    page_title="GrokVibes // INFINITE",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "search_term" not in st.session_state:
    st.session_state.search_term = ""
if "shuffle_trigger" not in st.session_state:
    st.session_state.shuffle_trigger = 0

# ==============================
# 2. THE MEGA-VAULT (80+ REAL NODES)
# ==============================
VAULT = [
    # --- GOD TIER (Headliners) ---
    {"n": "Juice WRLD", "cat": "Music", "tag": "Legend", "vibe": "Melodic Emo", "color": "#FF0055"},
    {"n": "Deftones", "cat": "Music", "tag": "Cult Classic", "vibe": "Ethereal Metal", "color": "#AA00FF"},
    {"n": "Playboi Carti", "cat": "Music", "tag": "Vamp", "vibe": "Rage", "color": "#FF3333"},
    {"n": "Frank Ocean", "cat": "Music", "tag": "Blond", "vibe": "Soulful", "color": "#FFAA00"},
    {"n": "Tyler, The Creator", "cat": "Music", "tag": "Igor", "vibe": "Alternative", "color": "#FF66AA"},
    
    # --- METALCORE / NU-METAL ---
    {"n": "Linkin Park", "cat": "Music", "tag": "Hybrid Theory", "vibe": "Nu-Metal", "color": "#D400FF"},
    {"n": "Bring Me The Horizon", "cat": "Music", "tag": "Sempiternal", "vibe": "Metalcore", "color": "#00CCFF"},
    {"n": "Knocked Loose", "cat": "Music", "tag": "Hardcore", "vibe": "Aggressive", "color": "#3344AA"},
    {"n": "Sleep Token", "cat": "Music", "tag": "Ritual", "vibe": "Atmospheric", "color": "#CCCCCC"},
    {"n": "Bad Omens", "cat": "Music", "tag": "Modern", "vibe": "Metal", "color": "#666666"},
    {"n": "Spiritbox", "cat": "Music", "tag": "Blue", "vibe": "Heavy", "color": "#3366FF"},
    {"n": "Loathe", "cat": "Music", "tag": "Experimental", "vibe": "Dreamy Heavy", "color": "#440044"},
    {"n": "System of a Down", "cat": "Music", "tag": "Political", "vibe": "Chaotic", "color": "#AA3300"},
    {"n": "Slipknot", "cat": "Music", "tag": "Maggot", "vibe": "Aggressive", "color": "#990000"},
    {"n": "Korn", "cat": "Music", "tag": "Freak", "vibe": "Nu-Metal", "color": "#660000"},
    {"n": "Limp Bizkit", "cat": "Music", "tag": "Energy", "vibe": "Nu-Metal", "color": "#FF0000"},
    {"n": "Static-X", "cat": "Music", "tag": "Industrial", "vibe": "Evil Disco", "color": "#000000"},
    {"n": "Evanescence", "cat": "Music", "tag": "Gothic", "vibe": "Rock", "color": "#000066"},
    
    # --- HIP HOP / EMO RAP ---
    {"n": "Lil Peep", "cat": "Music", "tag": "GBC", "vibe": "Grunge Rap", "color": "#FF66AA"},
    {"n": "XXXTENTACION", "cat": "Music", "tag": "BVF", "vibe": "Distorted", "color": "#AAAAAA"},
    {"n": "Kendrick Lamar", "cat": "Music", "tag": "Lyricist", "vibe": "Conscious", "color": "#009900"},
    {"n": "J. Cole", "cat": "Music", "tag": "Dreamville", "vibe": "Storytelling", "color": "#333333"},
    {"n": "A$AP Rocky", "cat": "Music", "tag": "Harlem", "vibe": "Cloud Rap", "color": "#6600CC"},
    {"n": "Denzel Curry", "cat": "Music", "tag": "Florida", "vibe": "High Energy", "color": "#FFCC00"},
    {"n": "Joey Bada$$", "cat": "Music", "tag": "Pro Era", "vibe": "Boom Bap", "color": "#CC9900"},
    {"n": "Yeat", "cat": "Music", "tag": "Twizzy", "vibe": "Rage", "color": "#FFFF00"},
    {"n": "Ken Carson", "cat": "Music", "tag": "Opium", "vibe": "Distorted", "color": "#000000"},
    {"n": "Destroy Lonely", "cat": "Music", "tag": "Opium", "vibe": "Fashion", "color": "#333333"},
    {"n": "Lucki", "cat": "Music", "tag": "Underground", "vibe": "Cloud Rap", "color": "#FF3366"},

    # --- CLOUD / GLITCH / PHONK ---
    {"n": "Crystal Castles", "cat": "Music", "tag": "Witch House", "vibe": "Glitch", "color": "#5500AA"},
    {"n": "Bladee", "cat": "Music", "tag": "Drain Gang", "vibe": "Cloud", "color": "#99CCFF"},
    {"n": "Yung Lean", "cat": "Music", "tag": "Sad Boys", "vibe": "Cloud Rap", "color": "#00FF99"},
    {"n": "Sewerslvt", "cat": "Music", "tag": "Breakcore", "vibe": "Draining", "color": "#990099"},
    {"n": "Kordhell", "cat": "Music", "tag": "Phonk", "vibe": "Drift", "color": "#33FF33"},
    {"n": "Pastel Ghost", "cat": "Music", "tag": "Darkwave", "vibe": "Ethereal", "color": "#CC00CC"},
    {"n": "Mr. Kitty", "cat": "Music", "tag": "Synthwave", "vibe": "Dark", "color": "#333333"},
    {"n": "Sidewalks and Skeletons", "cat": "Music", "tag": "Witch House", "vibe": "Goth", "color": "#000000"},

    # --- ANIME GOD TIER ---
    {"n": "Cyberpunk: Edgerunners", "cat": "Anime", "tag": "Trigger", "vibe": "Tragedy", "color": "#FNEE00"},
    {"n": "Chainsaw Man", "cat": "Anime", "tag": "Mappa", "vibe": "Chaos", "color": "#FF4400"},
    {"n": "Neon Genesis Evangelion", "cat": "Anime", "tag": "Classic", "vibe": "Psychological", "color": "#9933FF"},
    {"n": "Berserk (1997)", "cat": "Anime", "tag": "Seinen", "vibe": "Dark Fantasy", "color": "#990000"},
    {"n": "Cowboy Bebop", "cat": "Anime", "tag": "Sunrise", "vibe": "Noir Jazz", "color": "#FF9900"},
    {"n": "Samurai Champloo", "cat": "Anime", "tag": "Lofi", "vibe": "Chill", "color": "#FFCC33"},
    {"n": "Attack on Titan", "cat": "Anime", "tag": "Epic", "vibe": "War", "color": "#993333"},
    {"n": "Jujutsu Kaisen", "cat": "Anime", "tag": "Curse", "vibe": "Action", "color": "#330066"},
    {"n": "Vinland Saga", "cat": "Anime", "tag": "Viking", "vibe": "Historical", "color": "#6699FF"},
    {"n": "Hellsing Ultimate", "cat": "Anime", "tag": "Vampire", "vibe": "Gore", "color": "#990000"},
    {"n": "Devilman Crybaby", "cat": "Anime", "tag": "Netflix", "vibe": "Psychedelic", "color": "#FFFF00"},

    # --- ANIME AESTHETIC / CULT ---
    {"n": "Nana", "cat": "Anime", "tag": "Josei", "vibe": "Grunge", "color": "#770000"},
    {"n": "Paradise Kiss", "cat": "Anime", "tag": "Fashion", "vibe": "Romance", "color": "#3399FF"},
    {"n": "Serial Experiments Lain", "cat": "Anime", "tag": "Wired", "vibe": "Surreal", "color": "#44FF44"},
    {"n": "FLCL", "cat": "Anime", "tag": "Robot", "vibe": "Chaos", "color": "#FFEE00"},
    {"n": "Akira", "cat": "Anime", "tag": "Movie", "vibe": "Cyberpunk", "color": "#FF0000"},
    {"n": "Ghost in the Shell", "cat": "Anime", "tag": "Sci-Fi", "vibe": "Cyberpunk", "color": "#0099FF"},
    {"n": "Perfect Blue", "cat": "Anime", "tag": "Thriller", "vibe": "Psychological", "color": "#0033CC"},
    {"n": "Ergo Proxy", "cat": "Anime", "tag": "Goth", "vibe": "Mystery", "color": "#333333"},
    {"n": "Texhnolyze", "cat": "Anime", "tag": "Nihilism", "vibe": "Depressing", "color": "#666666"},
    {"n": "Initial D", "cat": "Anime", "tag": "Eurobeat", "vibe": "Drift", "color": "#FFFFFF"},
]

# ==============================
# 3. ADVANCED CSS (iOS GLASS 2.0)
# ==============================
st.markdown("""
<style>
    /* GLOBAL */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    [data-testid="stAppViewContainer"] {
        background-color: #050505;
        background-image: 
            radial-gradient(at 0% 0%, rgba(100, 0, 255, 0.1) 0px, transparent 50%),
            radial-gradient(at 90% 10%, rgba(255, 0, 85, 0.1) 0px, transparent 50%),
            radial-gradient(at 50% 100%, rgba(0, 255, 204, 0.05) 0px, transparent 50%);
        font-family: 'Inter', sans-serif;
        color: #ffffff;
    }
    
    [data-testid="stHeader"] { background: transparent; }

    /* SEARCH ISLAND */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 14px 20px !important;
        font-size: 15px !important;
        backdrop-filter: blur(12px);
    }
    .stTextInput > div > div > input:focus {
        border-color: #7000FF !important;
        background-color: rgba(255, 255, 255, 0.08) !important;
    }

    /* GLASS CARDS */
    .glass-card {
        background: rgba(30, 30, 30, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 20px;
        backdrop-filter: blur(16px);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .glass-card:hover {
        transform: translateY(-4px);
        background: rgba(40, 40, 40, 0.6);
        border-color: rgba(255, 255, 255, 0.2);
    }

    /* TYPOGRAPHY */
    .hero-title {
        font-size: 64px;
        font-weight: 900;
        letter-spacing: -2px;
        line-height: 1.1;
        background: linear-gradient(180deg, #fff, #888);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .card-title { font-size: 18px; font-weight: 700; color: #fff; margin-bottom: 4px; }
    .card-sub { font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; opacity: 0.7; }
    
    .tag-pill {
        font-size: 10px;
        padding: 4px 10px;
        background: rgba(255,255,255,0.1);
        border-radius: 20px;
        color: #ccc;
        font-weight: 600;
    }

    /* BUTTONS */
    .stButton > button {
        border-radius: 20px;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        color: white;
        transition: 0.3s;
    }
    .stButton > button:hover {
        border-color: #FF0055;
        color: #FF0055;
    }
</style>
""", unsafe_allow_html=True)

# ==============================
# 4. HERO SECTION (SPOTLIGHT)
# ==============================
spotlight = random.choice(VAULT)

col_hero_text, col_hero_card = st.columns([2, 1])

with col_hero_text:
    st.markdown('<div class="hero-title">GrokVibes<br>Infinite.</div>', unsafe_allow_html=True)
    st.markdown(f"Today's Spotlight: **{spotlight['n']}** // {spotlight['vibe']}")
    
    # Quick Filter Bar
    st.write("")
    f_cols = st.columns(6)
    filters = ["All", "Music", "Anime", "Metal", "Rap", "Chill"]
    
    for i, f in enumerate(filters):
        if f_cols[i].button(f, key=f"filter_{f}", use_container_width=True):
            if f == "All": st.session_state.search_term = ""
            elif f == "Metal": st.session_state.search_term = "metal" # generic search
            elif f == "Rap": st.session_state.search_term = "rap"
            else: st.session_state.search_term = f

with col_hero_card:
    # A larger visual card for the spotlight
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, {spotlight['color']}44, rgba(0,0,0,0)); border:1px solid {spotlight['color']}; border-radius:24px; padding:30px; text-align:center;">
        <div style="font-size:12px; letter-spacing:2px; margin-bottom:10px;">FEATURED</div>
        <div style="font-size:32px; font-weight:900;">{spotlight['n']}</div>
        <div style="margin-top:10px; opacity:0.8;">{spotlight['tag']}</div>
    </div>
    """, unsafe_allow_html=True)

# ==============================
# 5. MAIN CONTENT ENGINE
# ==============================
st.write("---")

col_search, col_shuffle = st.columns([4, 1])
with col_search:
    query_input = st.text_input("", placeholder="Search 80+ nodes (e.g. 'Phonk', '90s', 'Gore')...", value=st.session_state.search_term)
with col_shuffle:
    st.write("") # spacing
    if st.button("🎲 Shuffle", use_container_width=True):
        st.session_state.search_term = ""
        st.session_state.shuffle_trigger += 1

# Filtering Logic
query = query_input.lower()
filtered_vault = []

if not query and st.session_state.shuffle_trigger > 0:
    # Shuffle Mode
    filtered_vault = random.sample(VAULT, 24)
    st.caption("🎲 Displaying 24 random nodes from the Vault.")
elif query:
    # Search Mode
    for item in VAULT:
        blob = f"{item['n']} {item['cat']} {item['tag']} {item['vibe']}".lower()
        if query in blob:
            filtered_vault.append(item)
else:
    # Default Mode (Show Top 24)
    filtered_vault = VAULT[:24]

if not filtered_vault:
    st.warning(f"No frequency found for '{query}'. Try 'Chill', 'Anime', or 'Metal'.")
    filtered_vault = random.sample(VAULT, 8)

# ==============================
# 6. MASONRY GRID RENDER
# ==============================
cols = st.columns(4)

for i, item in enumerate(filtered_vault):
    col = cols[i % 4]
    with col:
        # Dynamic Styling
        border_color = item['color']
        
        # HTML Card
        st.markdown(f"""
        <div class="glass-card" style="border-top: 3px solid {border_color};">
            <div>
                <div class="card-sub" style="color:{border_color};">{item['cat']}</div>
                <div class="card-title">{item['n']}</div>
                <div style="margin-top:6px;"><span class="tag-pill">{item['vibe']}</span></div>
            </div>
            <div style="margin-top:20px; display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:11px; color:#888;">#{item['tag']}</span>
                <a href="https://www.youtube.com/results?search_query={item['n'].replace(' ', '+')}" target="_blank" style="text-decoration:none; color:white; opacity:0.6; font-size:18px;">↗</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add Button (Native Streamlit)
        if st.button("Add", key=f"add_{item['n']}_{i}"):
            if item not in st.session_state.favorites:
                st.session_state.favorites.append(item)
                st.toast(f"Saved {item['n']}", icon="🖤")

st.markdown("<br><br>", unsafe_allow_html=True)

# ==============================
# 7. SIDEBAR DASHBOARD
# ==============================
with st.sidebar:
    st.markdown("### 📡 Database Stats")
    c1, c2 = st.columns(2)
    c1.metric("Nodes", len(VAULT))
    c2.metric("Saved", len(st.session_state.favorites))
    
    st.divider()
    
    st.markdown("### 🖤 My Collection")
    if not st.session_state.favorites:
        st.caption("Your saved vibes appear here.")
    
    for fav in st.session_state.favorites:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:12px; margin-bottom:8px; border-left:2px solid {fav['color']};">
            <div style="font-weight:700; font-size:14px;">{fav['n']}</div>
            <div style="font-size:10px; opacity:0.7;">{fav['vibe']}</div>
        </div>
        """, unsafe_allow_html=True)
        
    if st.session_state.favorites:
        if st.button("Clear Collection", use_container_width=True):
            st.session_state.favorites = []
            st.rerun()
