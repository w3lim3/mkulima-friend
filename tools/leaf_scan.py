from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def diagnose_leaf(image_path: str, crop_hint: str = "") -> str:
    """
    Diagnose plant leaf problems using Gemma 4 Vision.
    """
    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        prompt = f"""
You are an expert plant pathologist helping smallholder farmers in Kenya.

Look carefully at this leaf photo.
Crop hint from farmer: {crop_hint if crop_hint else "Not specified"}

Please reply in this exact format:

**Possible Problem:** (name of disease or pest)
**Confidence:** (High / Medium / Low)
**Simple Explanation:** (explain in very simple language a farmer can understand)
**What the farmer can do now:** (2-4 practical steps)
**Warning:** (if serious, tell them to contact an agronomist)

If you are not sure, say Confidence: Low and recommend contacting a human expert.
"""

        response = client.models.generate_content(
            model="gemma-4-26b-a4b-it",
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                        types.Part.from_text(text=prompt)
                    ]
                )
            ]
        )
        return response.text

    except Exception as e:
        return f"Sorry, I could not analyse the photo. Error: {str(e)}"