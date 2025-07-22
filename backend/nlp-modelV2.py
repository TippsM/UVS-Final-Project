import json
from flask_cors import CORS
from flask import Flask, request, jsonify
from torch import nn
import torch
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForTokenClassification, AutoModelForSequenceClassification
import torch.nn.functional as F
from transformers import pipeline
import re

# NER model
tokenizer_ner = AutoTokenizer.from_pretrained("./backend/bert_model")
model_ner = AutoModelForTokenClassification.from_pretrained("./backend/bert_model")
model_ner.eval()

# vector model
model = SentenceTransformer(r"C:\all-MiniLM-L6-v2")

# # classification model 
# tokenizer = AutoTokenizer.from_pretrained(r"C:\Users\00432491\bart-large-mnli")
# model1 = AutoModelForSequenceClassification.from_pretrained(r"C:\Users\00432491\bart-large-mnli")
# classifier = pipeline("zero-shot-classification", model=model1, tokenizer=tokenizer, multi_label=True)

# Load vehicle specs

vehicle_ids = []

with open("Data/flat-vehicle-specs.txt", "r", encoding="utf-8") as f:
    text_to_embed = [line.strip() for line in f.readlines()]
    for line in text_to_embed:
        line = line.strip()
        if "Vehicle ID:" in line:
            vehicle_id = line.split("Vehicle ID:")[1].split(",")[0].strip()
            vehicle_ids.append(vehicle_id)

fields = [
    "Color", "Body Type", "Has Reefer", "Miles", "Year", "Make",
    "Engine Make", "Fuel Type", "Transmission Type", "Transmission Speeds",
    "Crew Cab", "Sleeper Cab", "Axles", "Brakes", "Gear Ratio"
]


app = Flask(__name__)
CORS(app)


#  ENTITY EXTRACTION 
def extract_entities(text):
    words = text.split()
    inputs = tokenizer_ner(words, return_tensors="pt", is_split_into_words=True, truncation=True)
    with torch.no_grad():
        outputs = model_ner(**inputs)

    logits = outputs.logits
    predictions = torch.argmax(logits, dim=2)[0].tolist()
    word_ids = inputs.word_ids()
    id2label = model_ner.config.id2label

    entities = {}
    current_label = None
    current_entity_tokens = []

    for idx, word_id in enumerate(word_ids):
        if word_id is None:
            continue

        label = id2label[predictions[idx]]

        if label.startswith("B-"):
            if current_label and current_entity_tokens:
                entities[current_label] = " ".join(current_entity_tokens)
            current_label = label[2:]
            current_entity_tokens = [words[word_id]]
        elif label.startswith("I-") and current_label:
            current_entity_tokens.append(words[word_id])
        else:
            if current_label and current_entity_tokens:
                entities[current_label] = " ".join(current_entity_tokens)
            current_label = None
            current_entity_tokens = []

    if current_label and current_entity_tokens:
        entities[current_label] = " ".join(current_entity_tokens)

    return entities

#  HELPER: get field value from line #
def get_field_value(text_line, field_name):
    pattern = rf"{field_name}:\s*([^,]+)"
    match = re.search(pattern, text_line, re.IGNORECASE)
    return match.group(1).strip() if match else ""




#  SEARCH WITH COMBINED SCORING 
def search(query, extracted_entities=None, top_k=10, entity_sim_threshold=0.5, entity_weight=0.6):
    clean_query = " ".join(extracted_entities.values()) if extracted_entities else query
    print("\nVector search using:", clean_query)

    query_embedding = model.encode(clean_query, convert_to_tensor=True)
    similarities = F.cosine_similarity(query_embedding.unsqueeze(0), embeddings)

    scores_combined = []
    for idx, vec_sim in enumerate(similarities):
        if extracted_entities:
            entity_sims = []
            match_text = text_to_embed[idx]
            for field, value in extracted_entities.items():
                candidate_value = get_field_value(match_text, field)
                if not candidate_value:
                    entity_sims.append(0)
                    continue

                entity_emb = model.encode(value, convert_to_tensor=True)
                candidate_emb = model.encode(candidate_value, convert_to_tensor=True)
                sim = F.cosine_similarity(entity_emb.unsqueeze(0), candidate_emb.unsqueeze(0)).item()
                entity_sims.append(sim)

            avg_entity_sim = sum(entity_sims) / len(entity_sims) if entity_sims else 0

            if avg_entity_sim < entity_sim_threshold:
                combined_score = -1.0
            else:
                combined_score = entity_weight * avg_entity_sim + (1 - entity_weight) * vec_sim
        else:
            combined_score = vec_sim

        scores_combined.append((idx, combined_score))

    filtered_scores = [(idx, score) for idx, score in scores_combined if score >= 0]

    filtered_scores.sort(key=lambda x: x[1], reverse=True)

    top_results = filtered_scores[:top_k]

    if not top_results:
        print("No filtered results matched all entities with threshold =", entity_sim_threshold)
        return [], []

    top_indices = [idx for idx, _ in top_results]
    top_scores = [score for _, score in top_results]

    return top_indices, top_scores


# FLASK API ROUTE 
@app.route("/search", methods=["POST"])
def search_route():
    data = request.get_json()
    query = data.get("query", "")

    if not query:
        return jsonify({"results": [], "error": "Query not provided"})

    extracted_entities = extract_entities(query)
    top_indices, top_scores = search(query, extracted_entities=extracted_entities)

    results = []
    for idx, score in zip(top_indices, top_scores):
        results.append({
            "match": text_to_embed[idx],
            "score": round(score, 4)
        })

    return jsonify({
        "results": results,
        "entities": extracted_entities
    })

if __name__ == "__main__":
    app.run(debug=True)