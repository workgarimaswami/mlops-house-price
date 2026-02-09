from flask import Flask, request, jsonify, send_from_directory
import pickle
import numpy as np
import os

app = Flask(__name__, static_folder='frontend', static_url_path='')

# Load model
try:
    with open('model/house_price_model.pkl', 'rb') as f:
        model = pickle.load(f)
    model_loaded = True
except:
    model_loaded = False

# Serve frontend files
@app.route('/')
def serve_frontend():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('frontend', path)

# API endpoints
@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'model_loaded': model_loaded})

@app.route('/api/predict', methods=['POST'])
def predict():
    if not model_loaded:
        return jsonify({'error': 'Model not loaded'}), 500
    
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