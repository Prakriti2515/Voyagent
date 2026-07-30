import os
from google import genai
from embeddings import get_query_embedding
from dotenv import load_dotenv
load_dotenv()

LLM_MODEL_NAME=os.environ["LLM_MODEL_NAME"]
def recommend_attractions(destination, api_key, vector_store=None):
    context_text = ""
    sources_used = []

    if vector_store is not None and not vector_store.is_empty():
        search_text = destination + " tourist attractions places to visit"
        query_embedding = get_query_embedding(search_text, api_key)
        matches = vector_store.search(query_embedding, top_k=3)

        for match in matches:
            context_text = context_text + match["text"] + "\n\n"
            if match["source"] not in sources_used:
                sources_used.append(match["source"])

    prompt = "You are a friendly local tour guide. Recommend the top tourist attractions in " + str(destination) + ".\n"
    prompt = prompt + "List 6 to 8 attractions, each with a short one line description.\n"

    if context_text != "":
        prompt = prompt + "\nHere is some info from uploaded travel guides, use it if relevant:\n" + context_text

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model=LLM_MODEL_NAME, contents=prompt)

    return {
        "attractions": response.text,
        "sources": sources_used
    }