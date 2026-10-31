# tools/region_knowledge.py
# Approximate, general knowledge for major farming counties in Kenya.
# Always confirm with the local county agriculture office / KALRO.

REGIONS = {
    "nairobi": {
        "zone": "Peri-urban, mid-highland",
        "rainfall": "Long rains Mar-May, short rains Oct-Dec (~900-1000 mm/yr)",
        "soils": "Red to dark clay-loams; black cotton soils in parts",
        "crops": ["kale (sukuma wiki)", "spinach", "tomatoes", "poultry", "dairy"],
        "tips": "Small plots: try vertical/sack gardens and drip irrigation. Good access to markets.",
    },
    "kiambu": {
        "zone": "Central highlands (upper midlands)",
        "rainfall": "Long rains Mar-May, short rains Oct-Dec (~1000-1500 mm/yr)",
        "soils": "Deep red volcanic loams, well drained, often slightly acidic",
        "crops": ["coffee", "tea", "dairy (napier)", "potatoes", "French beans", "vegetables"],
        "tips": "Acidic soils respond well to lime and manure. Watch for coffee berry disease and late blight in potatoes.",
    },
    "nakuru": {
        "zone": "Rift Valley highlands",
        "rainfall": "Main rains Mar-Sep, drier Dec-Feb (~700-1000 mm/yr)",
        "soils": "Volcanic loams; some sandy and alkaline soils around the lakes",
        "crops": ["maize", "wheat", "beans", "potatoes", "dairy", "pyrethrum"],
        "tips": "Frost can hit higher areas (Molo, Njoro). Plant early with the onset of rains.",
    },
    "nyeri": {
        "zone": "Central highlands, Mt Kenya slopes",
        "rainfall": "Long rains Mar-May, short rains Oct-Dec (~1000-1600 mm/yr)",
        "soils": "Deep, fertile red volcanic soils",
        "crops": ["coffee", "tea", "potatoes", "maize", "beans", "dairy", "macadamia"],
        "tips": "Steep slopes erode easily: use terraces and Napier grass strips.",
    },
    "muranga": {
        "zone": "Central highlands",
        "rainfall": "Long rains Mar-May, short rains Oct-Dec (~1000-1600 mm/yr)",
        "soils": "Deep red volcanic soils, fertile but acidic",
        "crops": ["coffee", "tea", "bananas", "avocado", "maize", "beans", "dairy"],
        "tips": "Avocado and banana do very well. Add lime to correct acidity.",
    },
    "meru": {
        "zone": "Eastern slopes of Mt Kenya",
        "rainfall": "Long rains Mar-May, short rains Oct-Dec (~800-2000 mm/yr, varies with altitude)",
        "soils": "Volcanic loams in the highlands; sandier, drier soils lower down",
        "crops": ["miraa (khat)", "coffee", "tea", "bananas", "maize", "beans", "potatoes"],
        "tips": "Choose crops by altitude: tea/coffee up high, sorghum/millet and green grams in drier lower zones.",
    },
    "machakos": {
        "zone": "Semi-arid to semi-humid, eastern Kenya",
        "rainfall": "Unreliable. Short rains Oct-Dec are often the best (~500-1000 mm/yr)",
        "soils": "Sandy loams and red soils, low organic matter",
        "crops": ["green grams (ndengu)", "pigeon peas", "sorghum", "millet", "mangoes", "maize"],
        "tips": "Use drought-tolerant crops, water harvesting (terraces, zai pits, farm ponds) and mulching.",
    },
    "kisumu": {
        "zone": "Lake Basin, warm and low altitude",
        "rainfall": "Two seasons, Mar-May and Aug-Oct (~1000-1500 mm/yr)",
        "soils": "Clay and black cotton soils in plains; sandy loams in uplands",
        "crops": ["rice (Ahero, West Kano)", "sugarcane", "maize", "sorghum", "cassava", "fish farming", "indigenous vegetables"],
        "tips": "Black cotton soils waterlog: use raised beds and good drainage. Watch for malaria-season labour planning.",
    },
    "uasin gishu": {
        "zone": "Highland plateau, Rift Valley (Eldoret)",
        "rainfall": "One main season Apr-Aug, reliable (~900-1200 mm/yr)",
        "soils": "Deep, well-drained red loams",
        "crops": ["maize", "wheat", "barley", "potatoes", "dairy", "sunflower"],
        "tips": "Big grain area: rotate maize with legumes or wheat to reduce disease build-up.",
    },
    "trans nzoia": {
        "zone": "Highland, north-west Kenya (Kitale)",
        "rainfall": "Reliable, Apr-Oct (~1000-1500 mm/yr)",
        "soils": "Deep red loams, naturally fertile",
        "crops": ["maize", "wheat", "beans", "sunflower", "dairy", "vegetables"],
        "tips": "Excellent maize area. Watch for maize lethal necrosis and stalk borers; use certified seed.",
    },
    "kakamega": {
        "zone": "Western highlands, high rainfall",
        "rainfall": "Heavy and well spread (~1200-2000 mm/yr)",
        "soils": "Red/brown loams, often acidic and leached",
        "crops": ["sugarcane", "maize", "beans", "tea", "bananas", "indigenous vegetables"],
        "tips": "Acidic soils: lime plus organic manure. Intercrop beans with maize to fix nitrogen.",
    },
    "bungoma": {
        "zone": "Western highlands (Mt Elgon slopes)",
        "rainfall": "Reliable, Mar-Oct (~1200-1800 mm/yr)",
        "soils": "Fertile loams on the slopes, clay in lower parts",
        "crops": ["maize", "sugarcane", "coffee", "beans", "sunflower", "dairy"],
        "tips": "Plant at the start of the long rains. Control erosion on the Mt Elgon slopes.",
    },
    "embu": {
        "zone": "Mt Kenya southern/eastern slopes",
        "rainfall": "Long rains Mar-May, short rains Oct-Dec (~800-1500 mm/yr)",
        "soils": "Volcanic red soils up high; drier sandy soils lower down",
        "crops": ["coffee", "tea", "macadamia", "maize", "beans", "cotton (lower zone)", "dairy"],
        "tips": "Lower Embu is drier: choose drought-tolerant crops and use mulch.",
    },
    "kirinyaga": {
        "zone": "Mt Kenya southern slopes",
        "rainfall": "Good, two seasons (~1000-1800 mm/yr)",
        "soils": "Volcanic loams, and clay soils in the Mwea rice plains",
        "crops": ["rice (Mwea)", "coffee", "tea", "French beans", "tomatoes", "bananas", "macadamia"],
        "tips": "Mwea is irrigated rice country. Manage water carefully and watch for rice blast.",
    },
    "narok": {
        "zone": "Rift Valley, plains and highlands (Mau)",
        "rainfall": "Moderate to good in the highlands, drier in the south",
        "soils": "Deep, fertile loams on the highland side",
        "crops": ["wheat", "barley", "maize", "potatoes", "livestock"],
        "tips": "Large-scale wheat and barley zone. Livestock keepers should plan for dry-season feed.",
    },
    "kajiado": {
        "zone": "Semi-arid",
        "rainfall": "Low and unreliable (~300-700 mm/yr)",
        "soils": "Sandy and shallow, low fertility",
        "crops": ["livestock", "drought-tolerant vegetables under irrigation", "sorghum", "millet"],
        "tips": "Irrigation (drip, boreholes), hay storage and drought-tolerant breeds are key.",
    },
    "mombasa": {
        "zone": "Coastal, hot and humid",
        "rainfall": "Long rains Apr-Jun, short rains Oct-Nov (~1000-1200 mm/yr)",
        "soils": "Sandy coastal soils and some clays; salinity near the shore",
        "crops": ["coconut", "cassava", "mangoes", "cashew", "vegetables"],
        "tips": "Sandy soils need lots of compost. Watch for salty water in irrigation.",
    },
    "kilifi": {
        "zone": "Coastal, hot and humid with a drier hinterland",
        "rainfall": "Long rains Apr-Jun, short rains Oct-Nov (~900-1200 mm/yr)",
        "soils": "Sandy loams on the coast, heavier soils inland",
        "crops": ["coconut", "cashew", "cassava", "mangoes", "maize", "green grams"],
        "tips": "Intercrop cashew/coconut with food crops. Use mulch to hold moisture.",
    },
}

# Common towns -> county, so "Thika" still works.
TOWN_TO_COUNTY = {
    "thika": "kiambu", "ruiru": "kiambu", "limuru": "kiambu", "kikuyu": "kiambu",
    "naivasha": "nakuru", "molo": "nakuru", "njoro": "nakuru", "gilgil": "nakuru",
    "karatina": "nyeri", "nanyuki": "laikipia", "othaya": "nyeri",
    "eldoret": "uasin gishu", "kitale": "trans nzoia",
    "mwea": "kirinyaga", "kerugoya": "kirinyaga",
    "kitui": "machakos", "athi river": "machakos", "mavoko": "machakos",
    "ongata rongai": "kajiado", "kitengela": "kajiado", "ngong": "kajiado",
    "maseno": "kisumu", "ahero": "kisumu",
    "webuye": "bungoma", "kimilili": "bungoma",
    "malindi": "kilifi", "mtwapa": "kilifi",
    "murang'a": "muranga", "muranga": "muranga",
    "nairobi": "nairobi",
}


def normalize_location(text: str):
    """Return a known county key from free text like 'Thika', 'Nakuru town', "Murang'a"."""
    if not text:
        return None
    t = text.lower().replace("county", "").replace("town", "").strip()
    t = t.replace("murang'a", "muranga")
    if t in REGIONS:
        return t
    if t in TOWN_TO_COUNTY:
        c = TOWN_TO_COUNTY[t]
        return c if c in REGIONS else None
    for key in REGIONS:
        if key in t:
            return key
    for town, county in TOWN_TO_COUNTY.items():
        if town in t and county in REGIONS:
            return county
    return None


def get_region_info(location: str) -> str:
    """Tool: returns farming info for a county/town as readable text."""
    key = normalize_location(location)
    if not key:
        return (
            f"I don't have detailed data for '{location}' yet. "
            "Give general advice and suggest the farmer confirm with their county agriculture office or KALRO."
        )
    r = REGIONS[key]
    return (
        f"Region: {key.title()} ({r['zone']})\n"
        f"Rainfall: {r['rainfall']}\n"
        f"Typical soils: {r['soils']}\n"
        f"Common crops: {', '.join(r['crops'])}\n"
        f"Local tip: {r['tips']}"
    )

import math

# Approximate centre point (lat, lon) of each county in REGIONS.
COUNTY_COORDS = {
    "nairobi": (-1.286, 36.817),
    "kiambu": (-1.170, 36.830),
    "nakuru": (-0.303, 36.080),
    "nyeri": (-0.420, 36.950),
    "muranga": (-0.720, 37.150),
    "meru": (0.050, 37.650),
    "machakos": (-1.520, 37.260),
    "kisumu": (-0.100, 34.760),
    "uasin gishu": (0.520, 35.270),
    "trans nzoia": (1.020, 34.950),
    "kakamega": (0.280, 34.750),
    "bungoma": (0.570, 34.560),
    "embu": (-0.530, 37.450),
    "kirinyaga": (-0.500, 37.280),
    "narok": (-1.080, 35.870),
    "kajiado": (-1.850, 36.780),
    "mombasa": (-4.040, 39.670),
    "kilifi": (-3.630, 39.850),
}


def _haversine_km(lat1, lon1, lat2, lon2):
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def county_from_gps(lat: float, lon: float, max_km: float = 120):
    """Return (county_key, distance_km) for the nearest supported county,
    or None if the point is outside Kenya or too far from any county we cover."""
    # Rough bounding box for Kenya
    if not (-4.9 <= lat <= 5.5 and 33.8 <= lon <= 42.0):
        return None
    best = min(
        ((key, _haversine_km(lat, lon, *coords)) for key, coords in COUNTY_COORDS.items()),
        key=lambda x: x[1],
    )
    return best if best[1] <= max_km else None


def parse_coordinates(text: str):
    """Turn '-1.28, 36.82' (or 'gps -1.28 36.82') into (lat, lon), else None."""
    cleaned = text.lower().replace("gps", "").replace(",", " ").split()
    try:
        lat, lon = float(cleaned[0]), float(cleaned[1])
        return lat, lon
    except (ValueError, IndexError):
        return None