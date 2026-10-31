import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts.system_prompt import SYSTEM_PROMPT

from tools.weather import get_weather
from tools.market import get_market_prices
from tools.leaf_scan import diagnose_leaf
from tools.soil import analyze_soil, diagnose_soil_photo
from tools.region_knowledge import get_region_info, normalize_location

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

def send_with_retry(chat, message, retries=3):
    """Retry on temporary Google server errors (500/503)."""
    for attempt in range(retries):
        try:
            return chat.send_message(message)
        except Exception as e:
            temporary = any(code in str(e) for code in ["500", "503", "INTERNAL", "UNAVAILABLE"])
            if temporary and attempt < retries - 1:
                time.sleep(2 ** attempt)  # wait 1s, then 2s
                continue
            raise


# ========== TOOL DEFINITIONS ==========
weather_tool = types.FunctionDeclaration(
    name="get_weather",
    description="Get current weather and 3-day forecast for a location in Kenya. Use this when the farmer asks about weather, rain, or temperature.",
    parameters={
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City or town name, e.g. Nairobi, Nakuru, Kisumu"}
        },
        "required": ["location"]
    }
)

market_tool = types.FunctionDeclaration(
    name="get_market_prices",
    description="Get current approximate market prices for crops in Kenya. Use when farmer asks about prices or selling.",
    parameters={
        "type": "object",
        "properties": {
            "crop": {"type": "string", "description": "Crop name e.g. maize, beans, tomatoes, potatoes, milk"},
            "location": {"type": "string", "description": "Market location e.g. Nairobi, Nakuru"}
        },
        "required": ["crop"]
    }
)

region_tool = types.FunctionDeclaration(
    name="get_region_info",
    description="Get farming knowledge for a Kenyan county or town: rainfall seasons, typical soils, common crops and local tips. Use for questions about what to plant, when to plant, or local conditions.",
    parameters={
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "County or town, e.g. Kiambu, Nakuru, Thika"}
        },
        "required": ["location"]
    }
)

soil_tool = types.FunctionDeclaration(
    name="analyze_soil",
    description=(
        "Analyse soil from the farmer's description and give advice. "
        "Before calling, ask the farmer (one or two questions at a time) about: soil colour, "
        "how it feels when squeezed wet (sandy / sticky clay / crumbly loam), and how water drains. "
        "Call this once you have at least colour and texture."
    ),
    parameters={
        "type": "object",
        "properties": {
            "colour": {"type": "string", "description": "e.g. red, dark brown, black, yellow, grey"},
            "texture": {"type": "string", "description": "e.g. sandy, sticky clay, crumbly loam, cracks when dry"},
            "drainage": {"type": "string", "description": "e.g. drains fast, waterlogged, slow to drain"},
            "ph_signs": {"type": "string", "description": "Any signs of acidity: moss, stunted yellow crops, etc."},
            "crop": {"type": "string", "description": "Crop the farmer wants to grow"},
            "location": {"type": "string", "description": "County or town"}
        },
        "required": ["colour", "texture"]
    }
)

# Register the actual functions
AVAILABLE_TOOLS = {
    "get_weather": get_weather,
    "get_market_prices": get_market_prices,
    "get_region_info": get_region_info,
    "analyze_soil": analyze_soil,
}

# Tools that should automatically receive the farmer's saved location
LOCATION_AWARE = {"get_weather", "get_market_prices", "get_region_info", "analyze_soil"}


def build_system_instruction(location: str) -> str:
    if not location:
        return SYSTEM_PROMPT
    region = get_region_info(location)
    return (
        SYSTEM_PROMPT
        + f"\n\nThe farmer is located in: {location}. Use this location by default for weather, "
          "market prices, planting advice and soil advice unless they mention another place."
        + f"\n\nRegional knowledge:\n{region}"
    )


def create_chat(location: str = ""):
    tools = types.Tool(function_declarations=[weather_tool, market_tool, region_tool, soil_tool])
    return client.chats.create(
        model=MODEL,
        config=types.GenerateContentConfig(
            system_instruction=build_system_instruction(location),
            tools=[tools]
        )
    )

def ask_location() -> str:
    while True:
        loc = input("Which county or town are you farming in? (e.g. Kiambu, Nakuru, Kisumu): ").strip()
        if not loc:
            continue
        key = normalize_location(loc)
        if key:
            print(f"Great, I'll use {key.title()} for weather, prices and farming advice.\n")
            return key.title()
        print(f"I don't have detailed data for '{loc}' yet, but I'll still use it for weather and prices.\n")
        return loc


def run_tools(chat, response, farmer_location):
    """Handle one or more tool calls until the model gives a text answer."""
    for _ in range(5):  # safety limit
        # Guard against empty or blocked responses
        if not response.candidates or not response.candidates[0].content:
            break
        parts = response.candidates[0].content.parts or []

        # The model may request several tools at once, so collect all of them
        function_calls = [p.function_call for p in parts if p.function_call]
        if not function_calls:
            break

        tool_responses = []
        for fc in function_calls:
            tool_name = fc.name
            tool_args = dict(fc.args or {})

            # Auto-fill saved location
            if tool_name in LOCATION_AWARE and not tool_args.get("location") and farmer_location:
                tool_args["location"] = farmer_location

            print(f"→ Calling tool: {tool_name} with {tool_args}")

            if tool_name in AVAILABLE_TOOLS:
                try:
                    tool_result = AVAILABLE_TOOLS[tool_name](**tool_args)
                except Exception as e:
                    tool_result = f"Tool error: {e}"
            else:
                tool_result = f"Unknown tool: {tool_name}"

            tool_responses.append(
                types.Part.from_function_response(
                    name=tool_name,
                    response={"result": tool_result}
                )
            )

        # Send every tool result back together
        response = send_with_retry(chat, tool_responses)
    return response

def main():
    print("🌱 Mkulima Friend is ready!")
    print("Ask about weather, market prices, soil, planting advice, or leaf problems.")
    print("Commands:")
    print("  scan <photo> [crop]       - diagnose a leaf photo")
    print("  soilphoto <photo> [crop]  - analyse a soil photo")
    print("  location <place>          - change your location")
    print("  quit                      - exit\n")

    farmer_location = ask_location()
    chat = create_chat(farmer_location)

    while True:
        user_input = input("Farmer: ").strip()
        lower = user_input.lower()

        if lower in ["quit", "exit", "bye"]:
            print("Asante sana! Take good care of your crops 🌾")
            break

        if not user_input:
            continue

        # Change location
        if lower.startswith("location "):
            new_loc = user_input[9:].strip()
            key = normalize_location(new_loc)
            farmer_location = key.title() if key else new_loc
            chat = create_chat(farmer_location)  # new chat so the model gets the new location
            print(f"\nLocation updated to {farmer_location}.\n")
            continue

        # Leaf scan
        if lower.startswith("scan ") or lower.startswith("diagnose "):
            parts = user_input.split()
            if len(parts) >= 2:
                image_path = parts[1]
                crop_hint = parts[2] if len(parts) > 2 else ""
                print("\nAnalysing leaf photo...")
                result = diagnose_leaf(image_path, crop_hint)
                print("\nMkulima Friend:", result)
                print("-" * 60)
                continue

        # Soil photo
        if lower.startswith("soilphoto "):
            parts = user_input.split()
            if len(parts) >= 2:
                image_path = parts[1]
                crop_hint = parts[2] if len(parts) > 2 else ""
                print("\nAnalysing soil photo...")
                result = diagnose_soil_photo(image_path, crop_hint, farmer_location)
                print("\nMkulima Friend:", result)
                print("-" * 60)
                continue

        try:
            response = send_with_retry(chat, user_input)
            response = run_tools(chat, response, farmer_location)
            print("\nMkulima Friend:", response.text)
            print("-" * 60)

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()