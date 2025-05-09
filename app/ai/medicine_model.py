from flask import current_app
from bson import ObjectId

class DiseaseMedicineModel:
    def __init__(self, mongo):
        # mongo is the PyMongo instance
        self.collection = mongo.db.disease_medicine

    def get_all_categories(self):
        return self.collection.distinct("category")

    def get_all_diseases(self):
        """Returns a list of all diseases with category and subcategory."""
        data = self.collection.find({})
        diseases = []
        for item in data:
            for disease in item.get("diseases", []):
                diseases.append({
                    "name": disease["name"],
                    "category": item["category"],
                    "sub_category": item["sub_category"]
                })
        return diseases

    def find_disease_by_name(self, disease_name):
        """Find disease by exact name."""
        doc = self.collection.find_one({
            "diseases.name": disease_name
        })
        if not doc:
            return None

        for disease in doc["diseases"]:
            if disease["name"].lower() == disease_name.lower():
                return {
                    "category": doc["category"],
                    "sub_category": doc["sub_category"],
                    **disease
                }
        return None

    def find_by_symptom(self, symptom):
        """Find diseases that have the given symptom."""
        matched = []
        cursor = self.collection.find({})
        for doc in cursor:
            for disease in doc.get("diseases", []):
                if any(symptom.lower() in s.lower() for s in disease.get("symptoms", [])):
                    matched.append({
                        "name": disease["name"],
                        "category": doc["category"],
                        "sub_category": doc["sub_category"],
                        "description": disease["description"],
                        "medicines": disease["medicines"]
                    })
        return matched
