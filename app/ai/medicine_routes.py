import random
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
                    # Friendly fallback messages
                    fallback_messages = [
                        """
                        ❌ <strong>Oops!</strong> I couldn’t find any diseases matching your input...<br><br>
                        But don’t worry, even the smartest AI gets a little confused sometimes 🤖💭<br>
                        Try rephrasing your symptoms — maybe use simpler words or describe them differently.<br><br>
                        Need inspiration? You can say things like:<br>
                        – “I have pain in my lower abdomen”<br>
                        – “I feel dizzy and nauseous”<br>
                        – “Skin is itching with red patches”<br><br>
                        I'm learning every day — thanks for your patience! 💙
                        """,

                        """
                        😅 <strong>No match found!</strong> But hey, Rome wasn’t diagnosed in a day! 🏛️<br><br>
                        Try giving me a bit more detail about your symptoms.<br>
                        Or describe it in a different way — I’ll do my best to help!<br><br>
                        If you're stuck, think about how you'd explain it to a doctor friend. 🩺
                        """,

                        """
                        🤔 Hmm... I didn’t quite catch that.<br><br>
                        Maybe I need more clues — like a detective on a case 🕵️<br>
                        Rephrase your symptoms or include more details like where or when it hurts.<br><br>
                        Together we’ll figure this out! 💡
                        """,

                        """
                        ⚠️ <strong>Sorry!</strong> I couldn’t connect your input to any known condition.<br><br>
                        But I’m not giving up on you!<br>
                        Try tweaking your description — sometimes small changes help big time! 🛠️<br><br>
                        And hey, you're awesome for trying 🧠✨
                        """
                    ]

                    # Pick one at random
                    response = random.choice(fallback_messages)
                    
    return render_template("ai/chatbot.html", user_input=user_input, response=response)


