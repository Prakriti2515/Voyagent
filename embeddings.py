
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()
EMBEDDING_DIMENSION = os.environ["EMBEDDING_DIMENSION"]
EMBEDDING_MODEL_NAME = os.environ["EMBEDDING_MODEL_NAME"]

def get_embedding(text, api_key):
    """
    used when we STORE document chunks in the vector database
    """
    client = genai.Client(api_key=api_key)

    result = client.models.embed_content(
        model=EMBEDDING_MODEL_NAME,
        contents=text,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT",
            output_dimensionality=EMBEDDING_DIMENSION
        )
    )

    return result.embeddings[0].values


def get_query_embedding(text, api_key):
    """
    used when the USER asks a question / searches for something
    (gemini uses a different task_type for search queries vs documents)
    """
    client = genai.Client(api_key=api_key)

    result = client.models.embed_content(
        model=EMBEDDING_MODEL_NAME,
        contents=text,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY",
            output_dimensionality=EMBEDDING_DIMENSION
        )
    )

    return result.embeddings[0].values