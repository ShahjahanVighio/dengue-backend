from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)

# Strict URL parsing defaults ko off karne ke liye strict_slashes false kiya
app.url_map.strict_slashes = False

# Frontend domains handling configuration
CORS(app, resources={r"/*": {"origins": "*"}})

HUMAN_TREATMENT_LOOKUP = {
    "mild": {
        "first_aid": [
            "Complete bed rest is highly recommended.",
            "Maintain high fluid intake: Drink ORS, coconut water, or fresh juices (2-3 liters/day).",
            "Take Paracetamol (Acetaminophen) 500mg every 6 hours for fever/pain reduction."
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
            "Apply constant direct pressure to any active mild bleeding sites (nose/gums) for 10 minutes."
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
            "Do NOT administer any fluids or food by mouth if the patient is lethargic or unconscious."
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
    Explicitly maps binary clinical vectors to exact probability scores.
    """
    # 1. Clean extracted values from safe dictionary unpacking
    fever = int(symptoms.get('fever', 0))
    headache = int(symptoms.get('headache', 0))
    joint_pain = int(symptoms.get('muscle_joint_pain', 0))
    mild_bleeding = int(symptoms.get('mild_bleeding', 0))
    difficulty_breath = int(symptoms.get('difficulty_breath', 0))
    stagnant_water = int(risk_factors.get('stagnant_water_zone', 0))
    
    # 2. Extract clinical score count based ONLY on checked parameters
    active_symptoms_count = fever + headache + joint_pain + mild_bleeding + difficulty_breath
    
    if active_symptoms_count == 0:
        return 0.0, "mild"
        
    # 3. Score weighting distribution logic
    # Total checked items in frontend are maximum 6
    total_checked = active_symptoms_count + stagnant_water
    probability = round((total_checked / 6.0) * 100, 2)
    
    # 4. Critical Pathway Mapping
    if difficulty_breath == 1 or probability >= 80.0:
        severity = "severe"
    elif mild_bleeding == 1 or probability >= 50.0:
        severity = "moderate"
    else:
        severity = "mild"
        
    return probability, severity

# Explicit matching standard patterns manually defined
@app.route('/predict/human', methods=['POST'])
def predict_human():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Missing JSON request payload"}), 400
            
        symptoms = data.get('symptoms', {})
        risk_factors = data.get('risk_factors', {})
        
        probability, severity = analyze_dengue_severity(symptoms, risk_factors)
        treatment_plan = HUMAN_TREATMENT_LOOKUP[severity]
        
        return jsonify({
            "status": "success",
            "risk_score_percentage": probability,
            "severity_level": severity,
            "treatment_plan": treatment_plan,
            "disclaimer": "This assessment is an AI-generated suggestion for educational reference. It is not a replacement for professional clinical laboratory tests."
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    return jsonify({"status": "active", "service": "Dengue Alert PK AI Core Engine Backend"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
