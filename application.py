from flask import Flask, request, jsonify
import pickle
import numpy as np
import os

app = Flask(__name__)

# Load model - adjust path if needed
try:
    with open('frontend/model/house_price_model.pkl', 'rb') as f:
        model = pickle.load(f)
    model_loaded = True
    print("Model loaded successfully!")
except Exception as e:
    model_loaded = False
    print(f"Error loading model: {e}")

@app.route('/')
def home():
    return "House Price Prediction API is running! Use POST /predict with JSON data."

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'model_loaded': model_loaded})

@app.route('/predict', methods=['POST'])
def predict():
    if not model_loaded:
        return jsonify({'error': 'Model not loaded. Check server logs.'}), 500
    
    try:
        data = request.get_json()
        features = data['features']  # Example: [3000, 3, 20] - [area, bedrooms, age]
        features_array = np.array(features).reshape(1, -1)
        prediction = model.predict(features_array)
        
        return jsonify({
            'prediction': float(prediction[0]),
            'status': 'success',
            'features_received': features
        })
        
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting server on port {port}...")
    app.run(host='0.0.0.0', port=port)