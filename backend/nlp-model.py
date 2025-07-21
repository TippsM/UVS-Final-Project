from flask_cors import CORS
from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import torch
import torch.nn.functional as F

# Load the data once
model = SentenceTransformer(r"nlp_model\all-MiniLM-L6-v2")
with open("../Data/flat-vehicle-specs.txt", "r", encoding="utf-8") as f:
    text_to_embed = [line.strip() for line in f.readlines()]
embeddings = model.encode(text_to_embed, convert_to_tensor=True)

app = Flask(__name__)
CORS(app)

@app.route("/search", methods=["POST"])
def search_route():
    
    data = request.get_json()
    query = data.get("query", "")

    if not query:
        return jsonify({"results": [], "error": "Query not provided"})

    query_embedding = model.encode(query, convert_to_tensor=True)
    similarities = F.cosine_similarity(query_embedding.unsqueeze(0), embeddings)
    top_k = 10
    top_results = torch.topk(similarities, k=min(top_k, len(similarities)))
    top_indices = top_results.indices.tolist()
    top_scores = top_results.values.tolist()

    results = []
    for idx, score in zip(top_indices, top_scores):
        results.append({
            "match": text_to_embed[idx],
            "score": round(score, 4)
        })

    return jsonify({"results": results})

if __name__ == "__main__":
    app.run(debug=True)
