
from flask import Flask, render_template, request, jsonify
import os

from pdf_reader import extract_text_from_pdf
from text_splitter import split_text_into_chunks
from embeddings import get_embedding
from vector_store import SimpleVectorStore
 
from orchestrator import process_chat_message
from agents.itinerary_agent import create_itinerary
from agents.comparison_agent import compare_destinations
from agents.budget_agent import estimate_budget
from agents.attraction_agent import recommend_attractions
from agents.weather_agent import get_weather

from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

EMBEDDING_DIMENSION = os.environ["EMBEDDING_DIMENSION"]

app = Flask(__name__)
 
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

vector_store = SimpleVectorStore(dimension=EMBEDDING_DIMENSION)
 
 
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_pdf():
    uploaded_files = request.files.getlist("pdf_files")
 
    if len(uploaded_files) == 0:
        return jsonify({"message": "No file selected"}), 400
 
    total_chunks_added = 0
 
    for pdf_file in uploaded_files:
        save_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
        pdf_file.save(save_path)
 
        full_text = extract_text_from_pdf(save_path)
        chunk_list = split_text_into_chunks(full_text, chunk_size=500, overlap=50)
 
        embedding_list = []
        for single_chunk in chunk_list:
            chunk_embedding = get_embedding(single_chunk, GEMINI_API_KEY)
            embedding_list.append(chunk_embedding)
 
        vector_store.add_chunks(chunk_list, embedding_list, pdf_file.filename)
        total_chunks_added = total_chunks_added + len(chunk_list)
 
    return jsonify({
        "message": "File(s) uploaded and processed successfully!",
        "chunks_added": total_chunks_added
    })

@app.route("/itinerary", methods=["POST"])
def itinerary_route():
    data = request.get_json()
    destination = data.get("destination", "")
    days = data.get("days", 3)
    interests = data.get("interests", "general sightseeing")
    budget_level = data.get("budget_level", "mid-range")
 
    result = create_itinerary(destination, days, interests, budget_level, vector_store, GEMINI_API_KEY)
    return jsonify(result)

@app.route("/compare", methods=["POST"])
def compare_route():
    data = request.get_json()
    destinations = data.get("destinations", [])
 
    result = compare_destinations(destinations, vector_store, GEMINI_API_KEY)
    return jsonify(result)

@app.route("/budget", methods=["POST"])
def budget_route():
    data = request.get_json()
    destination = data.get("destination", "")
    days = data.get("days", 3)
    travelers = data.get("travelers", 1)
    style = data.get("style", "mid-range")
 
    result = estimate_budget(destination, days, travelers, style, GEMINI_API_KEY)
    return jsonify(result)



if __name__ == "__main__":
    app.run(
        debug=True, 
        use_reloader=False
        )