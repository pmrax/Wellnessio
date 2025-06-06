from flask import Blueprint, request, render_template
from app.ai.medicine_model import DiseaseMedicineModel
from app import ai_mongo

ai_bp = Blueprint("ai", __name__, url_prefix="/ai")

@ai_bp.route("/chat", methods=["GET", "POST"])
def chatbot():
    disease_model = DiseaseMedicineModel(ai_mongo)
    response = None
    user_input = ""

    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip()

        if user_input:
            # Step 1: Attempt name-based detection
            disease_data = disease_model.find_disease_by_name(user_input)

            if disease_data:
                response = f"""
                🧾 <strong>Disease:</strong> {disease_data['name']}<br>
                📖 <strong>Description:</strong> {disease_data['description']}<br>
                🧬 <strong>Category:</strong> {disease_data['category']} / {disease_data['sub_category']}<br><br>
                💊 <strong>Medicines:</strong><br>
                """
                for med in disease_data.get('medicines', []):
                    response += f"- <strong>{med['name']}</strong> ({med['type']}): {med['dosage']} — {med.get('frequency', 'N/A')}<br>"

            else:
                # Step 2: Attempt symptom-based fuzzy matching
                matched_diseases = disease_model.smart_find_by_symptoms(user_input)

                if matched_diseases:
                    response = f"🩺 <strong>Possible conditions based on your symptoms:</strong> \"{user_input}\"<br><br>"

                    for res in matched_diseases[:3]:  # Top 3 only
                        explanation = disease_model.explain_match(res)
                        response += f"{explanation}<br><br>"
                        response += f"<em>Confidence Score:</em> {res['confidence_score']}%<br>"
                        response += f"<em>Description:</em> {res['description']}<br>"
                        response += f"<strong>Medicines:</strong><br>"
                        for med in res.get('medicines', []):
                            response += f"- {med['name']} ({med['type']}): {med['dosage']} — {med.get('frequency', 'N/A')}<br>"
                        response += "<hr>"

                else:
                    response = "❌ Sorry, I couldn't find any matching disease or symptoms. Try describing your issue differently."

    return render_template("ai/chatbot.html", user_input=user_input, response=response)
