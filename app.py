import streamlit as st
import requests

# === PASTE YOUR GROK API KEY HERE FOR LOCAL TESTING ===
# Get it from https://x.ai/api
# WARNING: Never commit this file with your real key! Keep it private/local.
API_KEY = "paste_your_grok_api_key_here"

if API_KEY == "paste_your_grok_api_key_here" or not API_KEY:
    st.error("""
    ⚠️ No Grok API key set!
    
    Paste your key directly into the API_KEY variable above (local testing only).
    
    For deployment: Use Streamlit Secrets instead—go to app settings > Secrets and add:
    ```
    GROK_API_KEY = "your_key_here"
    ```
    Then change the code to: API_KEY = st.secrets["GROK_API_KEY"]
    
    Get your key at https://x.ai/api
    """)
    st.stop()

# Grok API endpoint (double-check latest at https://x.ai/api)
API_URL = "https://api.x.ai/v1/chat/completions"

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
        "model": "grok-beta",  # Or latest—check docs
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.8,
        "max_tokens": 500
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"😓 API error: {str(e)} (Check key/model/endpoint at https://x.ai/api)"

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

st.caption("Open-source • Project #8 • For public repo: Use secrets instead of hardcoding!")
