import streamlit as st
import requests

# ==============================
# CONFIG
# ==============================

st.set_page_config(
    page_title="GrokVibes 💙",
    page_icon="🎧",
    layout="centered"
)

API_URL = "https://api.x.ai/v1/chat/completions"

# ==============================
# LOAD GROK API KEY (SECRETS ONLY)
# ==============================

API_KEY = st.secrets.get("GROK_API_KEY", "")

if not API_KEY:
    st.error("""
    ⚠️ **No Grok API key found**

    Add this to **Streamlit Secrets**:

    ```
    GROK_API_KEY = "your_key_here"
    ```

    • Local: `.streamlit/secrets.toml`  
    • Cloud: App → Settings → Secrets  

    Get your key at https://x.ai/api
    """)
    st.stop()

# ==============================
# GROK QUERY FUNCTION
# ==============================

def query_grok(user_input: str) -> str:
    system_prompt = """
    You are GrokVibes, an expert anime and music recommender.
    You specialize in:
    - cyberpunk
    - lo-fi
    - synthwave
    - emotional / late-night vibes

    For every response, provide:
    1. 3–5 anime recommendations with a one-line vibe match
    2. 3–5 music recommendations (artists, songs, or playlists)
    3. Optional: a "perfect pairing" (watch X while listening to Y)

    Keep it concise, chill, and stylish.
    Use emojis sparingly 🌃
    """

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "grok-2",  # change ONLY if xAI deprecates it
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ],
        "temperature": 0.8,
        "max_tokens": 500,
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        return f"😓 **Network/API error**:\n\n{e}"

    except (KeyError, IndexError):
        return "😓 **Unexpected API response format** — model or endpoint may have changed."

# ==============================
# UI
# ==============================

st.title("GrokVibes 🎧")
st.markdown(
    "*Powered by Grok • Anime + Music Recs • Built by @JoeyxHerrmann*"
)

st.write("Drop your vibe 👇  
*Examples:* `lo-fi cyberpunk anime`, `sad night drive`, `neon dystopia feels`")

user_input = st.text_input(
    "Your mood / vibe",
    placeholder="I love lo-fi and cyberpunk anime 🌃",
)

if st.button("Get Recs 🚀"):
    if user_input.strip():
        with st.spinner("Grok is mixing the perfect vibes..."):
            recs = query_grok(user_input)

        st.markdown("### 🎧 Your GrokVibes Recs")
        st.markdown(recs)

    else:
        st.warning("C’mon… give me a vibe 😏")

st.caption("Open-source • Secrets-only • Safe for public GitHub")
