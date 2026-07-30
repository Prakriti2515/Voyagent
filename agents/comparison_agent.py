import os
from google import genai
from embeddings import get_query_embedding
from dotenv import load_dotenv
load_dotenv()

LLM_MODEL_NAME=os.environ["LLM_MODEL_NAME"]

def compare_destinations(destination_list, vector_store, api_key):
    context_text = ""
    sources_used = []

    if not vector_store.is_empty():
        for place in destination_list:
            query_embedding = get_query_embedding(place + " travel information climate cost attractions", api_key)
            matches = vector_store.search(query_embedding, top_k=2)

            for match in matches:
                context_text = context_text + "[" + place + "] " + match["text"] + "\n\n"
                if match["source"] not in sources_used:
                    sources_used.append(match["source"])

    destinations_text = ", ".join(destination_list)

    prompt = "You are a travel expert. Compare the following destinations for a traveler: " + destinations_text + "\n\n"
    prompt = prompt + "Compare them using these points: weather/climate, average daily cost, best time to visit, top attractions, and who the destination is best suited for (families, couples, solo travelers, adventure seekers, etc).\n"
    prompt = prompt + "Use a clear heading for each destination, and end with a short recommendation on which one suits different types of travelers.\n"

    if context_text != "":
        prompt = prompt + "\nHere is some extra info from uploaded travel guides, use it if relevant:\n" + context_text

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model=LLM_MODEL_NAME, contents=prompt)

    return {
        "comparison": response.text,
        "sources": sources_used
    }