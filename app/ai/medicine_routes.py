from flask import Blueprint, request, render_template
from app.ai.medicine_model import DiseaseMedicineModel
from app import ai_mongo

ai_bp = Blueprint("ai", __name__, url_prefix="/ai")

@ai_bp.route("/chat", methods=["GET", "POST"])
def chatbot():
    # Create the model instance here, when ai_mongo is ready
    disease_model = DiseaseMedicineModel(ai_mongo)
    print("Mongo instance:", ai_mongo)
    print("Mongo DB:", ai_mongo.db)
    response = None
    user_input = ""

    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip()

        if user_input:
            # First try to find by disease name
            disease_data = disease_model.find_disease_by_name(user_input)

            if disease_data:
                response = f"🧾 Disease: {disease_data['name']}<br>" \
                           f"📖 Description: {disease_data['description']}<br>" \
                           f"🧬 Category: {disease_data['category']} / {disease_data['sub_category']}<br><br>" \
                           f"💊 Medicines:<br>"
                for med in disease_data['medicines']:
                    response += f"- <strong>{med['name']}</strong> ({med['type']}): {med['dosage']} — {med.get('frequency', 'N/A')}<br>"
            else:
                # If not found, try to match symptom
                results = disease_model.find_by_symptom(user_input)
                if results:
                    response = f"🩺 Found diseases matching symptom '{user_input}':<br><br>"
                    for res in results:
                        response += f"<strong>{res['name']}</strong>: {res['description']}<br>Medicines:<br>"
                        for med in res['medicines']:
                            response += f"- {med['name']} ({med['type']}): {med['dosage']}<br>"
                        response += "<br>"
                else:
                    response = "❌ Sorry, I couldn't find any matching disease or symptom."

    return render_template("ai/chatbot.html", user_input=user_input, response=response)



