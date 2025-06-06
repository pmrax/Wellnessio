import spacy
from rapidfuzz import fuzz
from flask import has_app_context

nlp = spacy.load("en_core_web_sm")

class DiseaseMedicineModel:
    def __init__(self, mongo):
        if not has_app_context():
            raise RuntimeError("Function called outside Flask app context.")
        if mongo.db is None:
            raise RuntimeError("Mongo client not initialized or app context missing")
        self.collection = mongo.db.disease_medicine

    def extract_symptoms(self, user_input):
        """Extract symptom-like phrases using NLP."""
        doc = nlp(user_input.lower())
        keywords = set()

        # Use noun_chunks (multi-word symptoms like "chest pain")
        for chunk in doc.noun_chunks:
            keywords.add(chunk.text.strip())

        # Also extract NOUN, ADJ, and VERB tokens that aren't stopwords
        for token in doc:
            if token.pos_ in ("NOUN", "ADJ", "VERB") and not token.is_stop:
                keywords.add(token.lemma_)

        return list(keywords)

    def fuzzy_match(self, user_symptom, disease_symptoms):
        """Return highest fuzzy similarity score for a single symptom."""
        return max([fuzz.token_sort_ratio(user_symptom, s) for s in disease_symptoms]) if disease_symptoms else 0

    def smart_find_by_symptoms(self, user_input, threshold=60, top_n=5):
        """Accept natural user input and return top N disease matches."""
        extracted_symptoms = self.extract_symptoms(user_input)
        results = []

        for doc in self.collection.find({}):
            for disease in doc.get("diseases", []):
                disease_symptoms = disease.get("symptoms", [])
                total_score, matches = 0, 0

                for symptom in extracted_symptoms:
                    score = self.fuzzy_match(symptom, disease_symptoms)
                    if score >= threshold:
                        matches += 1
                        total_score += score

                if matches:
                    confidence = round(total_score / matches, 2)
                    results.append({
                        "name": disease.get("name"),
                        "category": doc.get("category"),
                        "sub_category": doc.get("sub_category"),
                        "description": disease.get("description"),
                        "symptoms": disease.get("symptoms"),
                        "medicines": disease.get("medicines"),
                        "confidence_score": confidence,
                        "match_score": confidence,
                        "match_count": matches
                    })

        return sorted(results, key=lambda x: x["confidence_score"], reverse=True)[:top_n]

    def find_disease_by_name(self, name):
        """Find disease by exact or close name match within all records."""
        name = name.lower()
        cursor = self.collection.find({})
        best_match = None
        highest_score = 0

        for doc in cursor:
            for disease in doc.get("diseases", []):
                disease_name = disease.get("name", "").lower()
                score = fuzz.token_sort_ratio(name, disease_name)
                if score > highest_score:
                    highest_score = score
                    best_match = {
                        "name": disease.get("name"),
                        "description": disease.get("description"),
                        "category": doc.get("category"),
                        "sub_category": doc.get("sub_category"),
                        "medicines": disease.get("medicines", [])
                    }

        return best_match if highest_score >= 80 else None

    def explain_match(self, disease_obj):
        """Generate a natural language explanation with medicine details."""
        meds = disease_obj.get('medicines', [])
        med_lines = []

        for med in meds:
            if isinstance(med, dict):
                line = f"{med.get('name', 'Unnamed')} ({med.get('type', 'N/A')}, {med.get('dosage', 'N/A')})"
                med_lines.append(line)
            else:
                med_lines.append(str(med))  # fallback if it's a string

        return (f"Based on your symptoms, you may be experiencing **{disease_obj['name']}**, "
                f"a condition categorized under *{disease_obj['category']} → {disease_obj['sub_category']}*. "
                f"This condition is typically treated with: {', '.join(med_lines)}.")


