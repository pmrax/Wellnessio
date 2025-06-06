from flask import has_app_context

class DiseaseMedicineModel:
    def __init__(self, mongo):
        if not has_app_context():
            raise RuntimeError("Function called outside Flask app context.")
        if mongo.db is None:
            raise RuntimeError("Mongo client not initialized or app context missing")
        
        self.collection = mongo.db.disease_medicine

    def get_all_categories(self):
        """Returns all distinct categories."""
        return self.collection.distinct("category")

    def get_all_diseases(self):
        """Returns a list of all diseases with their category and subcategory."""
        diseases = []
        cursor = self.collection.find({})
        for item in cursor:
            for disease in item.get("diseases", []):
                diseases.append({
                    "name": disease.get("name"),
                    "category": item.get("category"),
                    "sub_category": item.get("sub_category")
                })
        return diseases

    def find_disease_by_name(self, disease_name):
        """Find a specific disease by exact name, returning its details."""
        doc = self.collection.find_one({
            "diseases.name": disease_name
        })
        if not doc:
            return None

        for disease in doc.get("diseases", []):
            if disease.get("name", "").lower() == disease_name.lower():
                return {
                    "category": doc.get("category"),
                    "sub_category": doc.get("sub_category"),
                    **disease
                }
        return None

    def find_by_symptom(self, symptom):
        """Find all diseases that have the given symptom (case-insensitive match)."""
        matched = []
        cursor = self.collection.find({})
        for doc in cursor:
            for disease in doc.get("diseases", []):
                symptoms = disease.get("symptoms", [])
                if any(symptom.lower() in s.lower() for s in symptoms):
                    matched.append({
                        "name": disease.get("name"),
                        "category": doc.get("category"),
                        "sub_category": doc.get("sub_category"),
                        "description": disease.get("description"),
                        "medicines": disease.get("medicines")
                    })
        return matched
