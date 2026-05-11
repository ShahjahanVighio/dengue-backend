from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)  # Taake Next.js is se connect kar sakay

# Model load karein
model = pickle.load(open('dengue_model.pkl', 'rb'))

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    # Data format: [fever, headache, joint_pain, bleeding]
    features = np.array([[data['fever'], data['headache'], data['joint_pain'], data['bleeding']]])
    prediction = model.predict(features)
    return jsonify({'dengue': int(prediction[0])})

if __name__ == '__main__':
    app.run(port=5000, debug=True)