def get_market_prices(crop: str = "maize", location: str = "Nairobi") -> str:
    """
    Returns approximate current market prices for common crops in Kenya.
    This is a simple mock for the hackathon. Later you can connect to a real API.
    """
    # Simple mock data (you can expand this later)
    prices = {
        "maize": {
            "Nairobi": "KSh 45 - 52 per kg",
            "Nakuru": "KSh 42 - 48 per kg",
            "Kisumu": "KSh 40 - 46 per kg",
            "default": "KSh 43 - 50 per kg"
        },
        "beans": {
            "Nairobi": "KSh 120 - 140 per kg",
            "Nakuru": "KSh 110 - 130 per kg",
            "default": "KSh 115 - 135 per kg"
        },
        "tomatoes": {
            "Nairobi": "KSh 60 - 90 per kg",
            "Nakuru": "KSh 50 - 80 per kg",
            "default": "KSh 55 - 85 per kg"
        },
        "potatoes": {
            "Nairobi": "KSh 35 - 50 per kg",
            "default": "KSh 30 - 45 per kg"
        },
        "milk": {
            "Nairobi": "KSh 50 - 60 per litre",
            "default": "KSh 45 - 55 per litre"
        }
    }

    crop = crop.lower().strip()
    location = location.title().strip()

    if crop not in prices:
        return f"Sorry, I don't have current price data for '{crop}'. I currently support: maize, beans, tomatoes, potatoes, and milk."

    crop_prices = prices[crop]
    price = crop_prices.get(location, crop_prices.get("default"))

    return f"""
Current approximate market price for {crop.title()} in {location}:
→ {price}

Note: Prices change daily. For the most accurate price, check your local market or ask nearby traders.
Would you like me to also estimate transport cost or advise when is a good time to sell?
"""