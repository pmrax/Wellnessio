from pymongo import MongoClient
from bson.regex import Regex

class MedicineModel:
    def __init__(self, db_uri="mongodb://localhost:27017/", db_name="wellnessio_ai", collection_name="disease_medicine"):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def get_medicines_by_disease(self, disease_name):
        """Find medicines for a given disease name (works for both flat and nested structure)."""
        # Try matching top-level disease
        result = self.collection.find_one({"disease": Regex(f"^{disease_name}$", "i")})
        if result:
            return {
                "disease": result["disease"],
                "description": result.get("description", ""),
                "medicines": result.get("medicines", [])
            }

        # Try nested search
        cursor = self.collection.find({"diseases.name": Regex(f"^{disease_name}$", "i")})
        for doc in cursor:
            for disease in doc.get("diseases", []):
                if disease["name"].lower() == disease_name.lower():
                    return {
                        "disease": disease["name"],
                        "symptoms": disease.get("symptoms", []),
                        "medicines": disease.get("medicines", [])
                    }
        return None

    def search_by_symptom(self, symptom_keyword):
        """Search for diseases and medicines based on a symptom keyword."""
        results = []

        # Search nested disease objects
        cursor = self.collection.find({"diseases.symptoms": {"$elemMatch": {"$regex": symptom_keyword, "$options": "i"}}})
        for doc in cursor:
            for disease in doc.get("diseases", []):
                if any(symptom_keyword.lower() in s.lower() for s in disease.get("symptoms", [])):
                    results.append({
                        "disease": disease["name"],
                        "symptoms": disease.get("symptoms", []),
                        "medicines": disease.get("medicines", [])
                    })

        return results
