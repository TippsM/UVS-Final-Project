import json
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

# classification model 
tokenizer = AutoTokenizer.from_pretrained(r"C:\Users\00432491\bart-large-mnli")
model1 = AutoModelForSequenceClassification.from_pretrained(r"C:\Users\00432491\bart-large-mnli")
classifier = pipeline("zero-shot-classification", model=model1, tokenizer=tokenizer, multi_label=True)

# Load vehicle specs
query = input("Search for a vehicle: ")
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


# MAIN 
extracted_entities = extract_entities(query)
print("Extracted entities:", extracted_entities)

embeddings = model.encode(text_to_embed, convert_to_tensor=True)
top_indices, top_scores = search(query, extracted_entities=extracted_entities)

print("\nSearch Results:")
if top_indices:
    for idx, score in zip(top_indices, top_scores):
        print(f"\nScore: {score:.4f}")
        print(f"Match: {text_to_embed[idx]}")
        print("--------")
else:
    print("No matches found.")

##code to read json into flat file and save into file to then feed into embedding 

# with open('Data/vehicle-specs.json','r') as f:
#     content=json.load(f)

# vehicles= content['VehicleNumber']

# print(f"Total vehicles in file: {len(vehicles)}")
# print(f"Sample vehicle IDs: {list(vehicles.keys())[:5]}")
# text_to_embed = []

# for vehicle_id, specs in vehicles.items():
#     price = specs.get("ASK PRICE", "")
#     body_height = specs.get("Body Height", "")
#     body_length = specs.get("Body Length", "")
#     body_type = specs.get("Body Type","")
#     brakes= specs.get("Brakes","")
#     axles = specs.get("Axle Count","")
#     make = specs.get("CHASSIS MAKE DESC","")
#     year = specs.get("Year","")
#     color =specs.get("Color","")
#     crew_cab = specs.get("Crew Cab","")
#     fuel = specs.get("Engine Fuel type","")
#     hp = specs.get("Engine HP","")
#     engine_make = specs.get("ENGINE MAKE DESC","")
#     sleeper = specs.get("Expediter/Sleeper Cab","")
#     gear_ratio = specs.get("Gear Ratio","")
#     #idk where the liftgate true/false is
#     has_reefer = specs.get("REEFER MAKE DESC") not in [None, "", "NaN"]
#     transmission_speed = specs.get("Transmission Speeds","")
#     transmission_type=specs.get("Transmission Type","")
#     miles = specs.get("UVS VEHICLE MILES","")

 


  


#     text = (
#     f"Vehicle ID: {vehicle_id}, "
#     f"Price: {price}, "
#     f"Body Height: {body_height}, "
#     f"Body Length: {body_length}, "
#     f"Body Type: {body_type}, "
#     f"Brakes: {brakes}, "
#     f"Axles: {axles}, "
#     f"Make: {make}, "
#     f"Year: {year}, "
#     f"Color: {color}, "
#     f"Crew Cab: {crew_cab}, "
#     f"Fuel Type: {fuel}, "
#     f"Engine HP: {hp}, "
#     f"Engine Make: {engine_make}, "
#     f"Sleeper Cab: {sleeper}, "
#     f"Gear Ratio: {gear_ratio}, "
#     f"Has Reefer: {'Yes' if has_reefer else 'No'}, "
#     f"Transmission Speeds: {transmission_speed}, "
#     f"Transmission Type: {transmission_type}, "
#     f"Miles: {miles}"
# )
#     text_to_embed.append(text)


# with open("flat-vehicle-specs.txt", "w", encoding="utf-8") as f:
#    for line in text_to_embed:
#         f.write(line + "\n")