import os
import json
from pymongo import MongoClient

# MongoDB connection
MONGO_URI = "mongodb+srv://pmrax001:pmrax001@ai.bmwjaxw.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["wellnessio_ai"]
collection = db["disease_medicine"]

# Path to your JSON folder
DATA_FOLDER = "./data"

def load_json_files(folder_path):
    data = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as file:
                try:
                    file_data = json.load(file)
                    data.extend(file_data)
                except Exception as e:
                    print(f"❌ Error reading {filename}: {e}")
    return data

def is_duplicate(entry):
    return collection.find_one({
        "category": entry["category"],
        "sub_category": entry["sub_category"],
        "diseases.name": {"$in": [d["name"] for d in entry["diseases"]]}
    }) is not None

def insert_unique_data(data):
    inserted_count = 0
    for entry in data:
        if not is_duplicate(entry):
            collection.insert_one(entry)
            inserted_count += 1
    return inserted_count

# Main logic
if __name__ == "__main__":
    all_data = load_json_files(DATA_FOLDER)
    new_records = insert_unique_data(all_data)
    print(f"✅ Inserted {new_records} new records into MongoDB.")
