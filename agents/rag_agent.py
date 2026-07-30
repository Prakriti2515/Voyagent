
from google import genai
from embeddings import get_query_embedding

LLM_MODEL_NAME="gemini-2.5-flash"
def answer_with_sources(question, vector_store, api_key):
 
    if vector_store.is_empty():
        client = genai.Client(api_key=api_key)
        prompt = "You are a friendly travel assistant. Answer this travel question: " + question
        response = client.models.generate_content(model=LLM_MODEL_NAME, contents=prompt)
        return {"answer": response.text, "sources": []}

   
    question_embedding = get_query_embedding(question, api_key)

    matches = vector_store.search(question_embedding, top_k=4)

    context_text = ""
    source_list = []

    for match in matches:
        context_text = context_text + match["text"] + "\n\n"
        if match["source"] not in source_list:
            source_list.append(match["source"])

    prompt = "You are a helpful travel assistant. Answer the question using the context below.\n"
    prompt = prompt + "If the answer is not fully in the context, use your general travel knowledge to fill in the gaps, but prefer the context when it is relevant.\n\n"
    prompt = prompt + "Context:\n" + context_text + "\n"
    prompt = prompt + "Question: " + question + "\n\nAnswer:"

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model=LLM_MODEL_NAME, contents=prompt)

    return {
        "answer": response.text,
        "sources": source_list
    }