from google import genai
LLM_MODEL_NAME="gemini-2.5-flash"

DAILY_COST_TABLE = {
    "budget":    {"stay": 20,  "food": 10, "local_transport": 5,  "activities": 10},
    "mid-range": {"stay": 60,  "food": 25, "local_transport": 10, "activities": 25},
    "luxury":    {"stay": 200, "food": 70, "local_transport": 30, "activities": 60}
}


def calculate_budget_numbers(days, travelers, style):
    style = str(style).lower()

    if style not in DAILY_COST_TABLE:
        style = "mid-range"

    costs = DAILY_COST_TABLE[style]

    stay_total = costs["stay"] * days
    food_total = costs["food"] * days * travelers
    transport_total = costs["local_transport"] * days * travelers
    activities_total = costs["activities"] * days * travelers

    grand_total = stay_total + food_total + transport_total + activities_total

    return {
        "style": style,
        "stay_total": stay_total,
        "food_total": food_total,
        "transport_total": transport_total,
        "activities_total": activities_total,
        "grand_total": grand_total
    }


def estimate_budget(destination, days, travelers, style, api_key):
  
    numbers = calculate_budget_numbers(days, travelers, style)

    prompt = "You are a travel budget expert. A traveler is planning this trip:\n"
    prompt = prompt + "Destination: " + str(destination) + "\n"
    prompt = prompt + "Days: " + str(days) + "\n"
    prompt = prompt + "Travelers: " + str(travelers) + "\n"
    prompt = prompt + "Style: " + str(style) + "\n\n"
    prompt = prompt + "Here is a cost breakdown already calculated in USD:\n"
    prompt = prompt + "Accommodation total: $" + str(numbers["stay_total"]) + "\n"
    prompt = prompt + "Food total: $" + str(numbers["food_total"]) + "\n"
    prompt = prompt + "Local transport total: $" + str(numbers["transport_total"]) + "\n"
    prompt = prompt + "Activities total: $" + str(numbers["activities_total"]) + "\n"
    prompt = prompt + "Grand total: $" + str(numbers["grand_total"]) + "\n\n"
    prompt = prompt + "Briefly explain this breakdown in a friendly way, then give 3 short money saving tips specific to this destination."

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model=LLM_MODEL_NAME, contents=prompt)

    return {
        "numbers": numbers,
        "explanation": response.text
    }