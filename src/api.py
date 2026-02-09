"""
Step 4: Create API for predictions
Think: Drive-thru window where customers order predictions
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import numpy as np
import pandas as pd
import os
import logging
from typing import List
import json

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="House Price Prediction API",
    description="API for predicting California house prices",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Global variables for model and scaler
model = None
scaler = None
model_metrics = {}

class HouseFeatures(BaseModel):
    """Input features for prediction"""
    MedInc: float = Field(..., description="Median income in block group", example=8.3252)
    HouseAge: float = Field(..., description="Median house age in block group", example=41.0)
    AveRooms: float = Field(..., description="Average number of rooms per household", example=6.9841)
    AveBedrms: float = Field(..., description="Average number of bedrooms per household", example=1.0238)
    Population: float = Field(..., description="Block group population", example=322.0)
    AveOccup: float = Field(..., description="Average number of household members", example=2.5556)
    Latitude: float = Field(..., description="Block group latitude", example=37.88)
    Longitude: float = Field(..., description="Block group longitude", example=-122.23)
    
    class Config:
        schema_extra = {
            "example": {
                "MedInc": 8.3252,
                "HouseAge": 41.0,
                "AveRooms": 6.9841,
                "AveBedrms": 1.0238,
                "Population": 322.0,
                "AveOccup": 2.5556,
                "Latitude": 37.88,
                "Longitude": -122.23
            }
        }

class PredictionResponse(BaseModel):
    """Response model for predictions"""
    prediction: float
    prediction_in_dollars: float
    confidence: float
    model_version: str
    timestamp: str
    features: dict

class BatchPredictionRequest(BaseModel):
    """Request model for batch predictions"""
    houses: List[HouseFeatures]

class BatchPredictionResponse(BaseModel):
    """Response model for batch predictions"""
    predictions: List[float]
    predictions_in_dollars: List[float]
    total_houses: int
    average_price: float
    model_version: str

# fix_api.py - Fix the syntax error in your API response

def fix_syntax_error():
    """
    The error was in line 24 of your terminal output.
    Fixed version:
    """
    correct_code = '''
    result = pred.json()
    print(f'2. Prediction: ${result["prediction_in_dollars"]:.2f}')
    print(f'3. Model Confidence: {result.get("confidence", "N/A")}')
    print('API is WORKING!')
    '''
    return correct_code

# Also update your api.py to ensure proper response format


def load_model():
    """Load the trained model and scaler"""
    global model, scaler, model_metrics
    
    try:
        # Load latest model
        model_path = "models/latest_model.pkl"
        scaler_path = "models/scaler.pkl"
        metrics_path = "models/latest_metrics.json"
        
        if not os.path.exists(model_path):
            logger.warning("Model not found. Training new model...")
            from train import main
            main()
        
        logger.info(f"Loading model from {model_path}")
        model = joblib.load(model_path)
        
        logger.info(f"Loading scaler from {scaler_path}")
        scaler = joblib.load(scaler_path)
        
        if os.path.exists(metrics_path):
            with open(metrics_path, 'r') as f:
                model_metrics = json.load(f)
            logger.info(f"Model metrics loaded: R²={model_metrics.get('r2', 'N/A')}")
        
        logger.info(f"✅ Model loaded successfully. Model type: {type(model).__name__}")
        logger.info(f"Model expects {model.n_features_in_} features")
        
    except Exception as e:
        logger.error(f"❌ Error loading model: {e}")
        raise

@app.on_event("startup")
async def startup_event():
    """Load model when the API starts"""
    logger.info("🚀 Starting House Price Prediction API...")
    load_model()

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to House Price Prediction API 🏠",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "This information",
            "GET /health": "API health check",
            "GET /model-info": "Model information",
            "POST /predict": "Predict house price for single house",
            "POST /predict-batch": "Predict prices for multiple houses",
            "GET /docs": "Interactive API documentation (Swagger UI)",
            "GET /redoc": "Alternative API documentation"
        },
        "example_request": {
            "url": "POST /predict",
            "body": {
                "MedInc": 8.3252,
                "HouseAge": 41.0,
                "AveRooms": 6.9841,
                "AveBedrms": 1.0238,
                "Population": 322.0,
                "AveOccup": 2.5556,
                "Latitude": 37.88,
                "Longitude": -122.23
            }
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    status = "healthy" if model is not None else "unhealthy"
    return {
        "status": status,
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None,
        "timestamp": pd.Timestamp.now().isoformat()
    }

@app.get("/model-info")
async def model_info():
    """Get information about the trained model"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "model_type": type(model).__name__,
        "model_features": model.n_features_in_ if hasattr(model, 'n_features_in_') else "Unknown",
        "training_date": model_metrics.get('timestamp', 'Unknown'),
        "performance": {
            "r2_score": model_metrics.get('r2', 'Unknown'),
            "rmse": model_metrics.get('rmse', 'Unknown'),
            "mae": model_metrics.get('mae', 'Unknown')
        },
        "feature_names": [
            "MedInc", "HouseAge", "AveRooms", "AveBedrms",
            "Population", "AveOccup", "Latitude", "Longitude"
        ]
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict_single(house: HouseFeatures):
    """
    Predict price for a single house
    
    - **MedInc**: Median income in block group
    - **HouseAge**: Median house age in block group
    - **AveRooms**: Average number of rooms
    - **AveBedrms**: Average number of bedrooms
    - **Population**: Block group population
    - **AveOccup**: Average number of household members
    - **Latitude**: Block group latitude
    - **Longitude**: Block group longitude
    """
    if model is None or scaler is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Please try again.")
    
    try:
        # Convert input to array
        features = np.array([[house.MedInc, house.HouseAge, house.AveRooms,
                            house.AveBedrms, house.Population, house.AveOccup,
                            house.Latitude, house.Longitude]])
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        
        # Convert from $1000s to actual dollars
        prediction_dollars = prediction * 1000
        
        # Calculate confidence based on R² score
        confidence = min(0.95, max(0.5, model_metrics.get('r2', 0.7)))
        
        return PredictionResponse(
            prediction=round(prediction, 2),
            prediction_in_dollars=round(prediction_dollars, 2),
            confidence=round(confidence, 2),
            model_version="1.0",
            timestamp=pd.Timestamp.now().isoformat(),
            features=house.dict()
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")

@app.post("/predict-batch", response_model=BatchPredictionResponse)
async def predict_batch(batch_request: BatchPredictionRequest):
    """
    Predict prices for multiple houses at once
    
    - Accepts a list of house features
    - Returns predictions for all houses
    """
    if model is None or scaler is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Extract features from all houses
        features_list = []
        for house in batch_request.houses:
            features_list.append([
                house.MedInc, house.HouseAge, house.AveRooms,
                house.AveBedrms, house.Population, house.AveOccup,
                house.Latitude, house.Longitude
            ])
        
        # Convert to numpy array
        features_array = np.array(features_list)
        
        # Scale features
        features_scaled = scaler.transform(features_array)
        
        # Make predictions
        predictions = model.predict(features_scaled)
        predictions_dollars = predictions * 1000
        
        return BatchPredictionResponse(
            predictions=[round(p, 2) for p in predictions.tolist()],
            predictions_in_dollars=[round(p, 2) for p in predictions_dollars.tolist()],
            total_houses=len(predictions),
            average_price=round(float(np.mean(predictions_dollars)), 2),
            model_version="1.0"
        )
        
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        raise HTTPException(status_code=400, detail=f"Batch prediction failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    # Run the API
    logger.info("Starting server on http://localhost:8000")
    logger.info("📚 API Documentation available at http://localhost:8000/docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",  # Listen on all network interfaces
        port=8000,
        log_level="info"
    )