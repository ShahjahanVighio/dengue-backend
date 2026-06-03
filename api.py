from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
# Vercel frontend se secure connections handle karne ke liye CORS configuration
CORS(app, resources={r"/*": {"origins": "*"}})

# Detailed Treatment & First Aid Lookup Table for Humans
HUMAN_TREATMENT_LOOKUP = {
    "mild": {
        "first_aid": [
            "Complete bed rest is highly recommended.",
            "Maintain high fluid intake: Drink ORS, coconut water, or fresh juices (2-3 liters/day).",
            "Take Paracetamol (Acetaminophen) 500mg every 6 hours for fever/pain reduction.",
            "Apply cool damp compresses to the forehead for high fever management.",
            "Use mosquito nets indoors to prevent further vector bites and virus transmission."
        ],
        "medications": {
            "allowed": ["Paracetamol (Acetaminophen)"],
            "forbidden": ["Aspirin", "Ibuprofen", "Naproxen", "Any other NSAIDs"]
        },
        "home_care": "Monitor urine output carefully (should be at least once every 6 hours). Check daily for warning signs like severe abdominal discomfort.",
        "referral": "Monitor closely. If the fever persists beyond 3 days or any acute warning sign appears, consult a doctor immediately."
    },
    "moderate": {
        "first_aid": [
            "Seek immediate medical consultation at a nearby clinic or emergency room.",
            "Continue oral hydration but strictly avoid dark sodas, caffeine, or acidic juices.",
            "Apply constant direct pressure to any active mild bleeding sites (nose/gums) for 10 minutes.",
            "Keep the patient resting on their side to maintain an open airway and prevent choking if vomiting occurs."
        ],
        "medications": {
            "allowed": ["Only clinical or prescribed medications"],
            "forbidden": ["Aspirin", "Ibuprofen", "Naproxen", "Any self-medicated painkillers"]
        },
        "home_care": "Clinical monitoring or brief hospital admission (24–48 hours) for blood counts and fluid stabilization may be required.",
        "referral": "Visit an outpatient facility, clinic, or Emergency Room within the next 12 hours."
    },
    "severe": {
        "first_aid": [
            "URGENT: Immediately seek professional emergency healthcare or call an ambulance.",
            "Lay the patient completely flat and elevate their legs slightly (shock recovery position).",
            "Do NOT administer any fluids or food by mouth if the patient is lethargic or unconscious.",
            "Apply firm, continuous manual pressure on any severe or actively bleeding sites.",
            "Keep the patient warm using a light blanket and turn their head to the side to avoid fluid aspiration."
        ],
        "medications": {
            "allowed": ["Emergency intravenous (IV) fluids and specialized critical care protocols in ICU"],
            "forbidden": ["All types of oral medications or self-treatment attempts"]
        },
        "home_care": "Strict Intensive Care Unit (ICU) metrics, precise fluid volume management, and oxygenation support.",
        "referral": "Call emergency services or rush directly to the nearest hospital Emergency ICU immediately."
    }
}

def analyze_dengue_severity(symptoms, risk_factors):
    """
    Evaluates the features to determine the conditional risk probability and severity category.
    """
    # Safety Check: Agar koi symptom selected nahi hy tou return 0% aur mild/none status
    symptoms_active_count = sum(symptoms.values())
    if symptoms_active_count == 0:
        return 0.0, "mild"

    severe_indicators = [
        symptoms.get('mucous_membrane_bleeding', 0),
        symptoms.get('difficulty_breath', 0),
        symptoms.get('restlessness', 0)
    ]
    
    moderate_indicators = [
        symptoms.get('mild_bleeding', 0),
        symptoms.get('easy_bruising', 0),
        symptoms.get('abdominal_pain', 0),
        symptoms.get('persistent_vomiting', 0)
    ]
    
    # Simple probability projection based on total matched features
    total_active_features = sum(symptoms.values()) + sum(risk_factors.values())
    total_possible_features = 19.0 # 15 symptoms + 4 risk factors
    
    probability = min((total_active_features / total_possible_features) * 100, 100.0)
    
    # Strict Clinical Decision Tree Matrix
    if any(severe_indicators) or probability >= 65.0:
        severity = "severe"
    elif any(moderate_indicators) or probability >= 30.0:
        # Agar severe indicators nahi hain aur mild symptoms hain tou it must be moderate threshold
        if symptoms_active_count <= 2 and not any(moderate_indicators):
            severity = "mild"
        else:
            severity = "moderate"
    else:
        severity = "mild"
        
    return round(probability, 2), severity

@app.route('/predict/human', methods=['POST'])
def predict_human():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Missing JSON request payload"}), 400
            
        symptoms = data.get('symptoms', {})
        risk_factors = data.get('risk_factors', {})
        
        # Calculate evaluation
        probability, severity = analyze_dengue_severity(symptoms, risk_factors)
        treatment_plan = HUMAN_TREATMENT_LOOKUP[severity]
        
        return jsonify({
            "status": "success",
            "risk_score_percentage": probability,
            "severity_level": severity,
            "treatment_plan": treatment_plan,
            "disclaimer": "This assessment is an AI-generated suggestion for educational reference and initial guidance. It is not a replacement for a professional medical diagnosis or clinical laboratory tests."
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Basic root endpoint check for validation
@app.route('/', methods=['GET'])
def index():
    return jsonify({"status": "active", "service": "Dengue Alert PK AI Core Engine Backend"}), 200

if __name__ == "__main__":
    # Dynamically reads the port parameter assigned by cloud providers like Railway
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
