from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, resources={r"/*": {"origins": "*"}})

HUMAN_TREATMENT_LOOKUP = {
    "mild": {
        "medications": {
            "allowed": ["Paracetamol (Acetaminophen)"],
            "forbidden": ["Aspirin", "Ibuprofen", "Naproxen", "Any other NSAIDs"]
        },
        "home_care": "Complete bed rest. Maintain high fluid intake (ORS, coconut water, fresh juices). Monitor urine output carefully.",
        "referral": "Monitor closely at home. If fever persists beyond 3 days, consult a physician."
    },
    "moderate": {
        "medications": {
            "allowed": ["Only clinical or prescribed medications"],
            "forbidden": ["Aspirin", "Ibuprofen", "Any self-medicated painkillers"]
        },
        "home_care": "Seek immediate medical consultation. Apply constant direct pressure to active mild bleeding sites.",
        "referral": "Visit an outpatient facility or Emergency Room within the next 12 hours."
    },
    "severe": {
        "medications": {
            "allowed": ["Emergency intravenous (IV) fluids and specialized critical care protocols in ICU"],
            "forbidden": ["All types of oral medications or self-treatment attempts"]
        },
        "home_care": "Strict Intensive Care Unit (ICU) metrics, precise fluid volume management, and oxygenation support.",
        "referral": "Call emergency services or rush directly to the nearest hospital Emergency ICU immediately."
    }
}

def analyze_dengue_severity(symptoms, risk_factors):
    # Flexible mapping supporting both camelCase from frontend and snake_case
    fever = int(symptoms.get('fever', 0))
    headache = int(symptoms.get('headache', 0))
    
    # Check both potential key mappings
    joint_pain = int(symptoms.get('muscle_joint_pain', symptoms.get('jointPain', 0)))
    mild_bleeding = int(symptoms.get('mild_bleeding', symptoms.get('bleeding', 0)))
    difficulty_breath = int(symptoms.get('difficulty_breath', symptoms.get('breathing', 0)))
    
    stagnant_water = int(risk_factors.get('stagnant_water_zone', risk_factors.get('waterZone', 0)))
    
    active_symptoms_count = fever + headache + joint_pain + mild_bleeding + difficulty_breath
    
    if active_symptoms_count == 0:
        return 0.0, "mild"
        
    total_checked = active_symptoms_count + stagnant_water
    probability = round((total_checked / 6.0) * 100, 2)
    
    # Clinical logic rules
    if difficulty_breath == 1 or probability >= 80.0:
        severity = "severe"
    elif mild_bleeding == 1 or probability >= 45.0:
        severity = "moderate"
    else:
        severity = "mild"
        
    return probability, severity

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
            "treatment_plan": treatment_plan
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    return jsonify({"status": "active", "service": "Dengue Alert PK AI Core Engine Backend"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
