# tools/soil.py
import os
import mimetypes
from dotenv import load_dotenv
from google import genai
from google.genai import types

from tools.region_knowledge import normalize_location, REGIONS

load_dotenv()
_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")


# ---------- PART A: question-based soil analysis (called as a tool) ----------
def analyze_soil(colour: str = "", texture: str = "", drainage: str = "",
                 ph_signs: str = "", crop: str = "", location: str = "") -> str:
    """Rule-based soil advice from what the farmer describes."""
    colour, texture = (colour or "").lower(), (texture or "").lower()
    drainage, ph_signs = (drainage or "").lower(), (ph_signs or "").lower()

    findings, actions = [], []

    # Colour
    if "red" in colour:
        findings.append("Red soil: usually well drained and rich in iron, but often acidic with low phosphorus.")
        actions.append("Add lime if the soil is acidic, plus manure/compost and a phosphorus source at planting.")
    elif "black" in colour or "dark" in colour:
        findings.append("Dark soil: usually high in organic matter and fertile.")
        if "clay" in texture or "sticky" in texture or "crack" in texture:
            findings.append("Sticky when wet and cracking when dry suggests black cotton soil, which waterlogs easily.")
            actions.append("Use raised beds and drainage channels. Avoid working the soil when wet.")
    elif "yellow" in colour or "pale" in colour or "white" in colour:
        findings.append("Pale or yellow soil: often leached and low in nutrients and organic matter.")
        actions.append("Build fertility with compost, manure and legume rotation (beans, groundnuts).")
    elif "grey" in colour or "mottled" in colour:
        findings.append("Grey or mottled soil: a sign of waterlogging.")
        actions.append("Improve drainage and plant on ridges or raised beds.")

    # Texture
    if "sand" in texture:
        findings.append("Sandy soil: drains fast, holds little water and few nutrients.")
        actions.append("Add plenty of compost/manure, mulch heavily and apply fertilizer in small, split doses.")
    elif "clay" in texture or "sticky" in texture:
        findings.append("Clay soil: holds water and nutrients but drains slowly and compacts.")
        actions.append("Add organic matter and sand/compost to open it up. Use ridges to improve drainage.")
    elif "loam" in texture:
        findings.append("Loamy soil: the best balance of water holding and drainage.")
        actions.append("Maintain it with crop rotation, compost and mulching.")

    # Drainage
    if "water" in drainage and ("log" in drainage or "stand" in drainage or "slow" in drainage):
        findings.append("Slow drainage or standing water risks root rot and disease.")
        actions.append("Dig drainage furrows and avoid planting root crops or beans in the wettest spots.")
    elif "slow" in drainage or "puddle" in drainage:
        findings.append("Slow drainage or standing water risks root rot and disease.")
        actions.append("Dig drainage furrows and avoid planting root crops or beans in the wettest spots.")
    elif "fast" in drainage or "dry" in drainage:
        findings.append("Fast drainage: crops may suffer in dry spells.")
        actions.append("Mulch, and consider drip irrigation or water harvesting.")

    # pH hints
    if any(w in ph_signs for w in ["acid", "moss", "sorrel", "yellow leaves", "stunted"]):
        actions.append("Signs point to acidity: lime is usually the first fix. A soil test will tell you how much.")

    # Region tie-in
    key = normalize_location(location)
    if key:
        findings.append(f"In {key.title()}, typical soils are: {REGIONS[key]['soils']}.")
    if crop:
        actions.append(f"For {crop}: apply manure or compost at planting and match fertilizer to a soil test result.")

    if not findings:
        return "I need a bit more detail: soil colour, how it feels (sandy/sticky/crumbly), and how water drains."

    actions.append("For exact fertilizer rates, do a soil test (county agriculture office, KALRO, or an accredited lab).")
    return "What I can tell from your description:\n- " + "\n- ".join(findings) + \
           "\n\nWhat to do:\n- " + "\n- ".join(dict.fromkeys(actions))


# ---------- PART B: photo-based soil analysis ----------
def diagnose_soil_photo(image_path: str, crop_hint: str = "", location: str = "") -> str:
    """Analyse a soil photo with the vision model."""
    if not os.path.exists(image_path):
        return f"I couldn't find the file '{image_path}'. Check the name and path."

    mime = mimetypes.guess_type(image_path)[0] or "image/jpeg"
    with open(image_path, "rb") as f:
        data = f.read()

    prompt = (
        "You are an agronomist helping a smallholder farmer in Kenya. "
        "Look at this soil photo and describe: likely colour/type, texture and structure, "
        "signs of low organic matter, compaction, erosion, waterlogging or salinity, "
        "and 3-5 practical, low-cost recommendations. Use simple language. "
        "Do not give exact fertilizer or lime amounts. "
        "Be honest that a photo cannot replace a lab soil test."
    )
    if location:
        prompt += f" The farm is in {location}."
    if crop_hint:
        prompt += f" The farmer wants to grow {crop_hint}."

    try:
        response = _client.models.generate_content(
            model=_MODEL,
            contents=[types.Part.from_bytes(data=data, mime_type=mime), prompt],
        )
        return response.text
    except Exception as e:
        return f"Sorry, I couldn't analyse the photo: {e}"