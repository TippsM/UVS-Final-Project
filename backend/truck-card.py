#code to read json into flat file and save into file to then feed into embedding 
import json

with open('../Data/truck-specs2.0.json','r') as f:
    content=json.load(f)

vehicles= content['VehicleNumber']

print(f"Total vehicles in file: {len(vehicles)}")
print(f"Sample vehicle IDs: {list(vehicles.keys())[:5]}")
text_to_embed = []

for vehicle_id, specs in vehicles.items():
    
    price = specs.get("ASK PRICE", "")
    img_url = specs.get("IMAGE URL1", "")
    make = specs.get("CHASSIS MAKE DESC","")
    year = specs.get("Year","")
    transmission_type = specs.get("Transmission Type","")
    miles = specs.get("UVS VEHICLE MILES","")
    vehicle_condition = specs.get("Vehicle Condition", "")
    model = specs.get("Model", "")
    gross_weight = specs.get("GVW", "")
    rear_axle_type = specs.get("Rear Axle Type", "")
  

    text = (
    f"Vehicle ID: {vehicle_id}, "
    f"Vehicle Condition: {vehicle_condition}, "
    f"Make: {make}, "
    f"Model: {model}, "
    f"Price: {price}, "
    f"Year: {year}, "
    f"Miles: {miles}, "
    f"Gross Weight: {gross_weight}, "
    f"Rear Axle Type: {rear_axle_type}, "
    f"Transmission Type: {transmission_type}, "
    f"Img Url: {img_url}"
)
    text_to_embed.append(text)



with open("truck-card-specs.txt", "w", encoding="utf-8") as f:
   for line in text_to_embed:
        f.write(line + "\n")