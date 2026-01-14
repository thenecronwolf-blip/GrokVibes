import streamlit as st
import os
import requests
from dotenv import load_dotenv

# Load env vars
load_dotenv()
API_KEY = os.getenv("GROK_API_KEY")

if not API_KEY:
    st.error("⚠️ Please add your Grok API key to .env file!")
    st.stop()

# Grok API endpoint (check latest at https://x.ai/api)
API_URL = "https://api.x.ai/v1/chat/completions"  # Confirm exact endpoint in docs

def query_grok(user_input):
    system_prompt = """
    You are GrokVibes, an expert anime and music recommender powered by Grok.
    Focus on lo-fi, cyberpunk, synthwave, and emotional vibes.
    For any user query, provide:
    1. 3-5 anime recommendations (series/movies) with a one-sentence vibe match.
    2. 3-5 music/track/playlist recommendations (artists, songs, YouTube/Spotify ideas).
    3. Optional: A short "perfect pairing" suggestion (e.g., watch X while listening to Y).
    Keep it chill, enthusiastic, and concise. Use emojis sparingly for neon flair 🌃
    """

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "grok-beta",  # Or latest model—check docs
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.8,  # Creative but coherent
        "max_tokens": 500
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"😓 API error: {str(e)} (Check key/model at https://x.ai/api)"

# Streamlit UI
st.set_page_config(page_title="GrokVibes 💙", page_icon="🎧", layout="centered")

st.title("GrokVibes")
st.markdown("*Powered by @grok • Anime + Music Recs • Built by @JoeyxHerrmann*")

st.write("Drop your vibe: e.g., 'I love lo-fi and cyberpunk anime' 🌃")

user_input = st.text_input("Your mood/vibe:", placeholder="I love lo-fi and cyberpunk #anime")

if st.button("Get Recs 🚀"):
    if user_input.strip():
        with st.spinner("Grok is mixing the perfect vibes..."):
            recs = query_grok(user_input)
        st.markdown("### 🎧 Your GrokVibes Recs")
        st.write(recs)
    else:
        st.warning("Tell me your vibe first! 😏")

st.caption("Open-source • Project #8 • Tweak the system prompt for more personality!")
