from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import os
# update
app = Flask(__name__)
# Sab origins allow kar dein taake Vercel se block na ho
CORS(app, resources={r"/*": {"origins": "*"}})

# Model load karein
try:
    model = pickle.load(open('dengue_model.pkl', 'rb'))
except Exception as e:
    print(f"Error loading model: {e}")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        # Features array banayein
        features = np.array([[
            data.get('fever', 0), 
            data.get('headache', 0), 
            data.get('joint_pain', 0), 
            data.get('bleeding', 0)
        ]])
        
        prediction = model.predict(features)
        return jsonify({'dengue': int(prediction[0])})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # Railway ke liye port aur host set karna zaroori hai
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
