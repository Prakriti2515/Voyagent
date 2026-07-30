
from google import genai
from embeddings import get_query_embedding

LLM_MODEL_NAME="gemini-2.5-flash"

def create_itinerary(destination, days, interests, budget_level, vector_store, api_key):
    context_text = ""
    sources_used = []

    if not vector_store.is_empty():
        search_text = destination + " travel guide attractions things to do"
        query_embedding = get_query_embedding(search_text, api_key)
        matches = vector_store.search(query_embedding, top_k=3)

        for match in matches:
            context_text = context_text + match["text"] + "\n\n"
            if match["source"] not in sources_used:
                sources_used.append(match["source"])

    prompt = "You are an expert travel planner. Create a detailed day-by-day itinerary.\n\n"
    prompt = prompt + "Destination: " + str(destination) + "\n"
    prompt = prompt + "Number of days: " + str(days) + "\n"
    prompt = prompt + "Traveler interests: " + str(interests) + "\n"
    prompt = prompt + "Budget level: " + str(budget_level) + "\n"

    if context_text != "":
        prompt = prompt + "\nHere is some extra information from uploaded travel guides, use it if relevant:\n" + context_text

    prompt = prompt + "\nFormat the itinerary clearly using Day 1, Day 2, etc, with Morning, Afternoon and Evening plans for each day."

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model=LLM_MODEL_NAME, contents=prompt)

    return {
        "itinerary": response.text,
        "sources": sources_used
    }