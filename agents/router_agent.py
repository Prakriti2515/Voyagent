
import json
from google import genai
LLM_MODEL_NAME="gemini-2.5-flash"

ROUTER_PROMPT = """You are the router for a travel planning assistant made of multiple agents.
Read the user's message and decide which ONE task it matches best.

Possible tasks:
- "itinerary"   -> user wants a trip plan / day by day itinerary for a destination
- "compare"     -> user wants to compare two or more destinations
- "budget"      -> user wants to estimate trip cost / budget
- "weather"     -> user wants current weather information for a place
- "attractions" -> user wants tourist attraction / places to visit recommendations
- "rag_qa"      -> user is asking a specific question that should be answered using uploaded travel documents
- "general"     -> small talk or anything that doesn't fit the above

Reply with ONLY a JSON object, nothing else, no explanation, in exactly this format:
{"task": "one_of_the_tasks_above"}

User message: """


def decide_task(user_message, api_key):
    client = genai.Client(api_key=api_key)

    full_prompt = ROUTER_PROMPT + user_message

    response = client.models.generate_content(
        model=LLM_MODEL_NAME,
        contents=full_prompt
    )

    raw_text = response.text.strip()

    raw_text = raw_text.replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(raw_text)
        return data.get("task", "general")
    except Exception:
        return "general"