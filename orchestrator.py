from agents.router_agent import decide_task
from agents.rag_agent import answer_with_sources
from agents.itinerary_agent import create_itinerary
from agents.comparison_agent import compare_destinations
from agents.budget_agent import estimate_budget
from agents.attraction_agent import recommend_attractions
from agents.weather_agent import get_weather


def extract_city_from_message(message):
    text = message.lower()

    words_to_remove = [
        "what is the weather in", "what's the weather in", "whats the weather in",
        "weather in", "weather at", "weather for", "how is the weather in",
        "weather", "?", "."
    ]

    for phrase in words_to_remove:
        text = text.replace(phrase, "")

    return text.strip().title()


def process_chat_message(user_message, vector_store, api_key):

    task = decide_task(user_message, api_key)

    if task == "itinerary":
        result = create_itinerary(
            destination=user_message,
            days=3,
            interests="general sightseeing",
            budget_level="mid-range",
            vector_store=vector_store,
            api_key=api_key
        )
        return {"agent_used": "Itinerary Agent", "answer": result["itinerary"], "sources": result["sources"]}

    elif task == "compare":
        cleaned = user_message.lower().replace(" versus ", " vs ")
        if " vs " in cleaned:
            places = cleaned.split(" vs ")
        else:
            places = user_message.split(",")

        places = [p.strip() for p in places if p.strip() != ""]

        if len(places) < 2:
            return {"agent_used": "Comparison Agent", "answer": "Please mention at least two destinations to compare, for example: 'Compare Goa vs Manali'.", "sources": []}

        result = compare_destinations(places, vector_store, api_key)
        return {"agent_used": "Comparison Agent", "answer": result["comparison"], "sources": result["sources"]}

    elif task == "budget":
        result = estimate_budget(
            destination=user_message,
            days=3,
            travelers=1,
            style="mid-range",
            api_key=api_key
        )
        answer_text = result["explanation"]
        return {"agent_used": "Budget Agent", "answer": answer_text, "sources": []}

    elif task == "weather":
        city = extract_city_from_message(user_message)
        weather_data = get_weather(city)

        if "error" in weather_data:
            return {"agent_used": "Weather Agent", "answer": weather_data["error"], "sources": []}

        answer_text = "Weather in " + weather_data["place"] + ": " + weather_data["condition"]
        answer_text = answer_text + ", " + str(weather_data["temperature_celsius"]) + "°C"
        answer_text = answer_text + ", wind " + str(weather_data["windspeed_kmh"]) + " km/h"

        return {"agent_used": "Weather Agent", "answer": answer_text, "sources": []}

    elif task == "attractions":
        result = recommend_attractions(user_message, api_key, vector_store)
        return {"agent_used": "Attraction Agent", "answer": result["attractions"], "sources": result["sources"]}

    elif task == "rag_qa":
        result = answer_with_sources(user_message, vector_store, api_key)
        return {"agent_used": "Agentic RAG", "answer": result["answer"], "sources": result["sources"]}

    else:
       
        result = answer_with_sources(user_message, vector_store, api_key)
        return {"agent_used": "General Assistant", "answer": result["answer"], "sources": result["sources"]}