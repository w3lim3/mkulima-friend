import os
import html
import tempfile
import streamlit as st
from streamlit_geolocation import streamlit_geolocation

# Copy Streamlit secrets into environment variables BEFORE importing main
try:
    for k, v in st.secrets.items():
        if isinstance(v, str):
            os.environ.setdefault(k, v)
except Exception:
    pass  # running locally with .env

from main import create_chat, run_tools, send_with_retry
from tools.region_knowledge import REGIONS, county_from_gps
from tools.leaf_scan import diagnose_leaf
from tools.soil import diagnose_soil_photo

st.set_page_config(page_title="Mkulima Friend", page_icon="🌱", layout="centered")

# ---------- Farm theme (CSS) ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #fdf8e8 0%, #f4f8e8 60%, #e9f3d9 100%);
}
[data-testid="stBottom"] > div {
    background: transparent;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #dcedc8 0%, #f1f8e9 100%);
    border-right: 3px solid #8bc34a;
}
[data-testid="stSidebar"] h2 {
    color: #2e5d1e;
}

/* ---------- Hero banner (landing screen) ---------- */
.hero {
    position: relative;
    overflow: hidden;
    border-radius: 20px;
    padding: 28px 24px 70px 24px;
    background: linear-gradient(180deg, #87ceeb 0%, #cdeefd 55%, #fff6d6 100%);
    box-shadow: 0 4px 14px rgba(46, 93, 30, 0.25);
    margin-bottom: 8px;
}
.hero .sun {
    position: absolute;
    top: 16px;
    right: 28px;
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background: radial-gradient(circle, #fff176 40%, #ffd54f 100%);
    box-shadow: 0 0 30px 10px rgba(255, 213, 79, 0.6);
}
.hero-text { position: relative; z-index: 2; }
.hero-text h1 {
    margin: 0;
    color: #1b5e20;
    font-size: 2.2rem;
}
.hero-text p {
    margin: 4px 0 10px 0;
    color: #33691e;
    font-size: 1.05rem;
}
.badge {
    display: inline-block;
    background: rgba(255, 255, 255, 0.85);
    color: #2e5d1e;
    border-radius: 999px;
    padding: 4px 14px;
    font-weight: 600;
    font-size: 0.9rem;
}
.hills {
    position: absolute;
    left: 0;
    bottom: 0;
    width: 100%;
    height: 70px;
}
.crops {
    text-align: center;
    font-size: 1.7rem;
    letter-spacing: 10px;
    margin: 4px 0 6px 0;
}

/* ---------- Compact header (once chatting) ---------- */
.compact {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: linear-gradient(90deg, #dcedc8 0%, #f1f8e9 100%);
    border: 1px solid #c5e1a5;
    border-radius: 16px;
    padding: 10px 16px;
    margin-bottom: 14px;
    color: #1b5e20;
}

/* ---------- Landing (Grok-style centre) ---------- */
.landing-title {
    text-align: center;
    font-size: 2rem;
    font-weight: 700;
    color: #1b5e20;
    margin: 26px 0 4px 0;
}
.landing-sub {
    text-align: center;
    color: #33691e;
    margin-bottom: 18px;
}

/* Big rounded input bar */
[data-testid="stChatInput"] {
    border-radius: 30px !important;
    border: 2px solid #8bc34a !important;
    background: #ffffff !important;
    box-shadow: 0 6px 20px rgba(46, 93, 30, 0.18);
}
[data-testid="stChatInput"] textarea {
    font-size: 1.05rem !important;
    padding-top: 14px !important;
    padding-bottom: 14px !important;
}

.welcome {
    background: #ffffffcc;
    border-left: 6px solid #7cb342;
    border-radius: 12px;
    padding: 14px 18px;
    margin: 10px 0 14px 0;
    color: #2b3a1f;
}
[data-testid="stChatMessage"] {
    background: #ffffffd9;
    border: 1px solid #c5e1a5;
    border-radius: 16px;
    padding: 10px 14px;
}
div.stButton > button {
    border-radius: 999px;
    border: 1.5px solid #7cb342;
    background: #f1f8e9;
    color: #2e5d1e;
    font-weight: 600;
}
div.stButton > button:hover {
    background: #7cb342;
    color: white;
    border-color: #558b2f;
}
.footer {
    text-align: center;
    color: #6b7d55;
    font-size: 0.8rem;
    margin-top: 24px;
}

/* ---------- Green fonts ---------- */

/* Sidebar: headings, labels, radio options, captions, normal text */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color: #1b5e20 !important;
}

/* Sidebar inputs: text typed in boxes and dropdown */
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] textarea,
[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #1b5e20 !important;
}
[data-testid="stSidebar"] input::placeholder {
    color: #6a9a5b !important;
}

/* Sidebar buttons: keep text white on hover */
[data-testid="stSidebar"] div.stButton > button:hover p {
    color: white !important;
}

/* Farmer's request (chat box) */
[data-testid="stChatInput"] textarea {
    color: #1b5e20 !important;
    font-weight: 500;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #6a9a5b !important;
}

/* Chat messages: both the farmer's messages and the AI's replies */
[data-testid="stChatMessage"],
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3,
[data-testid="stChatMessage"] h4,
[data-testid="stChatMessage"] strong,
[data-testid="stChatMessage"] em,
[data-testid="stChatMessage"] td,
[data-testid="stChatMessage"] th {
    color: #1b5e20 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar: location + photo analysis ----------
with st.sidebar:
    st.header("🏡 Your farm")
    method = st.radio("Set my location", ["Pick my county", "Use my GPS"])

    location = ""
    if method == "Pick my county":
        counties = sorted(k.title() for k in REGIONS)
        choice = st.selectbox("County", counties + ["Other"])
        location = st.text_input("Type your county or town") if choice == "Other" else choice
    else:
        st.caption("Tap the button and allow location access in your browser.")
        geo = streamlit_geolocation()
        lat, lon = geo.get("latitude"), geo.get("longitude")
        if lat is not None and lon is not None:
            match = county_from_gps(lat, lon)
            if match:
                key, dist = match
                location = key.title()
                st.success(f"Looks like you are near {location} (about {dist:.0f} km from the county centre).")
                st.caption("Not right? Switch to 'Pick my county'.")
            else:
                st.warning("I couldn't match your GPS to a county I support yet. Please pick your county instead.")

    st.divider()
    st.header("📸 Photo check")
    photo_type = st.radio("What is in the photo?", ["🍃 Leaf (crop disease)", "🌍 Soil"])
    crop_hint = st.text_input("Crop (optional)", placeholder="e.g. maize")
    photo = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png"])
    if photo:
        st.image(photo, use_container_width=True)
    analyse = st.button("🔍 Analyse photo", disabled=photo is None, use_container_width=True)

# ---------- Session state (reset chat if location changes) ----------
if st.session_state.get("location") != location:
    st.session_state.location = location
    st.session_state.chat = create_chat(location or "")
    st.session_state.messages = []

# ---------- Photo analysis ----------
if analyse and photo:
    suffix = os.path.splitext(photo.name)[1] or ".jpg"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(photo.getvalue())
        path = tmp.name
    with st.spinner("Analysing photo... 🌿"):
        try:
            if "Leaf" in photo_type:
                result = diagnose_leaf(path, crop_hint)
            else:
                result = diagnose_soil_photo(path, crop_hint, location or "")
        except Exception as e:
            result = f"Sorry, I couldn't analyse that photo: {e}"
        finally:
            os.remove(path)
    st.session_state.messages.append({"role": "user", "content": f"📷 {photo_type} photo uploaded"})
    st.session_state.messages.append({"role": "assistant", "content": result})

# ---------- Pick up a question submitted on the previous run ----------
pending = st.session_state.pop("pending_prompt", None)
need_reply = False
if pending:
    st.session_state.messages.append({"role": "user", "content": pending})
    need_reply = True

badge_text = f"📍 {html.escape(location)}" if location else "📍 Choose your location in the sidebar"

QUICK_ACTIONS = {
    "☔ Weather": "What is the weather forecast for my farm this week?",
    "💰 Prices": "What are the current market prices for maize and beans?",
    "🌍 Soil": "I want to check my soil.",
    "🌽 What to plant": "What should I plant this season in my area?",
}

# ======================================================================
# LANDING SCREEN: hero + centred input (Grok style)
# ======================================================================
if not st.session_state.messages:
    st.markdown(f"""
<div class="hero">
<div class="sun"></div>
<div class="hero-text">
<h1>🌱 Mkulima Friend</h1>
<p>Your farming companion · Rafiki wa Mkulima</p>
<span class="badge">{badge_text}</span>
</div>
<svg class="hills" viewBox="0 0 1200 120" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
<path d="M0,70 C150,10 300,110 500,60 C700,10 850,100 1200,40 L1200,120 L0,120 Z" fill="#9ccc65"/>
<path d="M0,95 C200,50 400,120 650,85 C850,55 1000,110 1200,80 L1200,120 L0,120 Z" fill="#689f38"/>
<path d="M0,112 C300,90 600,120 900,105 C1050,98 1150,108 1200,104 L1200,120 L0,120 Z" fill="#33691e"/>
</svg>
</div>
<div class="crops">🌽 🍅 🥔 🫘 🥬 🍌 ☕</div>
<div class="landing-title">What can I help you grow today?</div>
<div class="landing-sub">Karibu! Ask about weather, prices, soil, planting or crop problems.</div>
""", unsafe_allow_html=True)

    # Inside a container, chat_input is shown in place (not pinned to the bottom)
    with st.container():
        landing_prompt = st.chat_input("Ask Mkulima Friend anything about your farm...", key="chat_landing")
    if landing_prompt:
        st.session_state.pending_prompt = landing_prompt
        st.rerun()

    cols = st.columns(len(QUICK_ACTIONS))
    for col, (label, text) in zip(cols, QUICK_ACTIONS.items()):
        if col.button(label, use_container_width=True):
            st.session_state.pending_prompt = text
            st.rerun()

# ======================================================================
# CHAT SCREEN: compact header + history
# ======================================================================
else:
    st.markdown(
        f'<div class="compact"><span>🌱 <b>Mkulima Friend</b></span>'
        f'<span class="badge">{badge_text}</span></div>',
        unsafe_allow_html=True,
    )

    for m in st.session_state.messages:
        avatar = "🌱" if m["role"] == "assistant" else "🧑‍🌾"
        with st.chat_message(m["role"], avatar=avatar):
            st.markdown(m["content"])

    # Generate the AI reply for the question just submitted
    if need_reply:
        with st.chat_message("assistant", avatar="🌱"):
            with st.spinner("Thinking... 🌾"):
                try:
                    chat = st.session_state.chat
                    response = run_tools(chat, send_with_retry(chat, pending), location)
                    reply = response.text or "Sorry, I couldn't come up with an answer. Please try asking again."
                except Exception as e:
                    reply = f"Sorry, something went wrong: {e}"
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

    # Input pinned to the bottom once the conversation has started
    bottom_prompt = st.chat_input("Ask about weather, prices, soil, crops...", key="chat_bottom")
    if bottom_prompt:
        st.session_state.pending_prompt = bottom_prompt
        st.rerun()

st.markdown(
    '<div class="footer">🌾 Advice is general guidance. For exact chemical or fertilizer amounts, '
    'talk to your local agricultural extension officer.</div>',
    unsafe_allow_html=True,
)