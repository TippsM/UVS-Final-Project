import json
from torch import nn
import torch
from sentence_transformers import SentenceTransformer
import os
import torch.nn.functional as F
import math
 

# Search query (example search bar..)
query = input("Search for a vehicle: ")

   
with open("../Data/flat-vehicle-specs.txt", "r", encoding="utf-8") as f:
    text_to_embed = [line.strip() for line in f.readlines()]




model = SentenceTransformer(r"C:\Users\00431753\all-MiniLM-L6-v2")
embeddings = model.encode(text_to_embed, convert_to_tensor = True)




def search(query, top_k=10):
    query_embedding = model.encode(query, convert_to_tensor=True)
    similarities = F.cosine_similarity(query_embedding.unsqueeze(0), embeddings)

    actual_k = min(top_k, len(similarities))
    if actual_k == 0:
        return [], []

    top_results = torch.topk(similarities, k=actual_k)
    top_indices = top_results.indices.tolist()
    top_scores = top_results.values.tolist()
    return top_indices, top_scores


top_indices, top_scores = search(query)

for idx, score in zip(top_indices, top_scores):
    print(f"Score: {score:.4f * 100}")
    print(f"Match: {text_to_embed[idx]}")
    print("--------")


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