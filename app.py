import streamlit as st
import random
import re

# ==============================
# 1. APP CONFIGURATION
# ==============================
st.set_page_config(
    page_title="GrokVibes // INTELLIGENT",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if "favorites" not in st.session_state: st.session_state.favorites = []
if "search_term" not in st.session_state: st.session_state.search_term = ""

# ==============================
# 2. INTELLIGENT VAULT (With Hidden 'Keywords' for Smart Matching)
# ==============================
# I've added a 'kw' (keywords) list to ensure specific searches like "weird sad rap" hit the right targets.
VAULT = [
    # --- SPECIFIC TARGETS FOR "SAD WEIRD RAP" ---
    {"n": "Destroy Lonely", "cat": "Music", "tag": "Opium", "vibe": "Fashion Demon", "color": "#333333", 
     "kw": ["sad", "weird", "rap", "dark", "fashion", "distorted", "opium", "rage"]},
    
    {"n": "Earl Sweatshirt", "cat": "Music", "tag": "Doris", "vibe": "Depressing Lyrical", "color": "#554433", 
     "kw": ["sad", "weird", "rap", "lyrical", "abstract", "depressing", "lofi"]},
    
    {"n": "Tyler, The Creator", "cat": "Music", "tag": "Igor", "vibe": "Alt-HipHop", "color": "#FF66AA", 
     "kw": ["weird", "rap", "sad", "love", "alternative", "colorful"]},

    {"n": "Yung Lean", "cat": "Music", "tag": "Sad Boys", "vibe": "Cloud Rap", "color": "#00FF99", 
     "kw": ["sad", "weird", "rap", "cloud", "sweden", "emotional"]},

    # --- OTHER GOD TIER NODES ---
    {"n": "Juice WRLD", "cat": "Music", "tag": "999", "vibe": "Melodic Emo", "color": "#FF0055",
     "kw": ["sad", "rap", "emo", "melodic", "heartbreak", "freestyle"]},

    {"n": "Deftones", "cat": "Music", "tag": "White Pony", "vibe": "Ethereal Metal", "color": "#AA00FF",
     "kw": ["horny", "sad", "metal", "shoegaze", "dreamy", "heavy"]},

    {"n": "Playboi Carti", "cat": "Music", "tag": "Vamp", "vibe": "Rage", "color": "#FF3333",
     "kw": ["hype", "weird", "rap", "punk", "vampire", "rage"]},

    {"n": "Crystal Castles", "cat": "Music", "tag": "Cult", "vibe": "Witch House", "color": "#5500AA",
     "kw": ["weird", "sad", "electronic", "glitch", "chaotic"]},

    {"n": "Sewerslvt", "cat": "Music", "tag": "Draining", "vibe": "Breakcore", "color": "#990099",
     "kw": ["sad", "weird", "electronic", "fast", "depressing"]},

    {"n": "Knocked Loose", "cat": "Music", "tag": "Hardcore", "vibe": "Aggressive", "color": "#3344AA",
     "kw": ["angry", "heavy", "metal", "gym", "workout"]},
     
    {"n": "Chainsaw Man", "cat": "Anime", "tag": "Mappa", "vibe": "Chaos", "color": "#FF4400",
     "kw": ["weird", "action", "blood", "demon", "sad"]},

    {"n": "Neon Genesis Evangelion", "cat": "Anime", "tag": "Nerv", "vibe": "Psychological", "color": "#9933FF",
     "kw": ["sad", "weird", "mecha", "depressing", "classic"]},
     
    {"n": "Berserk (1997)", "cat": "Anime", "tag": "Eclipse", "vibe": "Dark Fantasy", "color": "#990000",
     "kw": ["sad", "dark", "pain", "struggle", "guts"]},
]

# ==============================
# 3. THE VIBE ENGINE (Smart Scoring)
# ==============================
def vibe_check(query, data):
    if not query:
        return data # Return everything if empty
    
    query_words = set(query.lower().split())
    scored_results = []
    
    for item in data:
        score = 0
        # Check hidden keywords
        item_keywords = set(item['kw'] + [item['n'].lower(), item['vibe'].lower()])
        
        # Calculate intersection (how many words match?)
        matches = query_words.intersection(item_keywords)
        score += len(matches) * 10 # Base score for keyword match
        
        # Boost for exact name match
        if query.lower() in item['n'].lower():
            score += 50
            
        if score > 0:
            scored_results.append((score, item))
            
    # Sort by score (highest match first)
    scored_results.sort(key=lambda x: x[0], reverse=True)
    return [x[1] for x in scored_results]

# ==============================
# 4. VISUAL STYLING (iOS GLASS)
# ==============================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    [data-testid="stAppViewContainer"] {
        background-color: #050505;
        background-image: 
            radial-gradient(at 0% 0%, rgba(50, 0, 100, 0.2) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(0, 50, 100, 0.2) 0px, transparent 50%);
        font-family: 'Inter', sans-serif;
        color: #fff;
    }
    
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px;
        backdrop-filter: blur(20px);
        transition: transform 0.2s;
        height: 100%;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        border-color: rgba(255, 255, 255, 0.3);
        background: rgba(255, 255, 255, 0.05);
    }
    
    .match-badge {
        background: #00FFCC; color: black; 
        font-size: 10px; font-weight: bold; 
        padding: 2px 8px; border-radius: 10px;
        margin-bottom: 5px; display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# ==============================
# 5. UI IMPLEMENTATION
# ==============================
st.title("GrokVibes // INTELLIGENT")
st.markdown("Try searching complex vibes like: **'sad weird rap'**, **'heavy angry gym'**, or **'classic sad anime'**.")

# Input
query_input = st.text_input("", placeholder="Describe the vibe...", value=st.session_state.search_term)

# Process Results
results = vibe_check(query_input, VAULT)

# Top Result Spotlight (If a search is active)
if query_input and results:
    top_match = results[0]
    st.markdown("### 🔥 Top Match")
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, {top_match['color']}44, rgba(0,0,0,0)); border-left: 5px solid {top_match['color']}; padding: 25px; border-radius: 15px; margin-bottom: 30px;">
        <div style="font-size: 12px; font-weight: bold; letter-spacing: 2px; color: {top_match['color']};">100% VIBE MATCH</div>
        <div style="font-size: 40px; font-weight: 900; margin: 5px 0;">{top_match['n']}</div>
        <div style="font-size: 16px; opacity: 0.8;">{top_match['vibe']} • {top_match['tag']}</div>
        <div style="margin-top: 15px; font-size: 12px; font-family: monospace; opacity: 0.5;">
            MATCHED KEYWORDS: {', '.join(top_match['kw'][:5])}...
        </div>
    </div>
    """, unsafe_allow_html=True)

# Grid Results
st.markdown("### 📡 Results")
if not results:
    st.warning("No vibes found. Try broadening your search.")
else:
    cols = st.columns(4)
    for i, item in enumerate(results[:20]): # Show top 20 matches
        col = cols[i % 4]
        with col:
            st.markdown(f"""
            <div class="glass-card" style="border-top: 2px solid {item['color']};">
                <div style="color:{item['color']}; font-size:10px; font-weight:700; margin-bottom:5px;">{item['cat'].upper()}</div>
                <div style="font-weight:800; font-size:18px;">{item['n']}</div>
                <div style="font-size:12px; opacity:0.7; margin-top:5px;">{item['vibe']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Save", key=f"save_{i}"):
                if item not in st.session_state.favorites:
                    st.session_state.favorites.append(item)
                    st.toast(f"Added {item['n']}")

# Sidebar
with st.sidebar:
    st.header("Saved Vibes")
    for fav in st.session_state.favorites:
        st.write(f"♥ {fav['n']}")
