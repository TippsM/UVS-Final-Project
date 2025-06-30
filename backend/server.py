from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Pre-encoded truck data
trucks = [
    "Class 8, Sleeper Cab, Diesel, D13 Engine, 500 HP, I-Shift Transmission, Long-Haul",
    "Class 5, Box Truck, Refrigerated, Diesel, 20ft Cargo Box, Thermo King, Urban Delivery",
    "Cargo Van, High Roof, Extended Length, 3.5L EcoBoost, Gasoline, 487 cu ft, Delivery Van"
]
truck_embeddings = model.encode(trucks)

@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    query = data.get("query", "")
    query_embedding = model.encode([query])[0]
    scores = util.cos_sim(query_embedding, truck_embeddings)[0].cpu().numpy()

    best_index = int(scores.argmax())
    return jsonify({
        "best_match": trucks[best_index],
        "similarity_scores": [float(s) for s in scores]
    })

if __name__ == "__main__":
    app.run(debug=True)
