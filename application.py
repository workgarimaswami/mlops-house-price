from flask import Flask, request, jsonify
import pickle
import numpy as np
import os

app = Flask(__name__)

# Load model
try:
    with open('model/house_price_model.pkl', 'rb') as f:
        model = pickle.load(f)
    model_loaded = True
except:
    model_loaded = False

@app.route('/')
def home():
    return "House Price Prediction API"

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        features = data['features']
        features_array = np.array(features).reshape(1, -1)
        prediction = model.predict(features_array)
        return jsonify({'prediction': float(prediction[0])})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)