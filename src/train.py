"""
Complete model training pipeline
"""
import pandas as pd
import numpy as np
import joblib
import os
import logging
import json
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_processed_data():
    """Load preprocessed data"""
    logger.info("📂 Loading processed data...")
    
    processed_path = "data/processed"
    
    # Check if processed data exists
    if not os.path.exists(f"{processed_path}/X_train.csv"):
        logger.error("❌ Processed data not found!")
        logger.info("Running preprocessing first...")
        from preprocess import main
        return main()
    
    X_train = pd.read_csv(f"{processed_path}/X_train.csv")
    X_test = pd.read_csv(f"{processed_path}/X_test.csv")
    y_train = pd.read_csv(f"{processed_path}/y_train.csv").squeeze()
    y_test = pd.read_csv(f"{processed_path}/y_test.csv").squeeze()
    
    logger.info(f"✅ Data loaded: Train={X_train.shape}, Test={X_test.shape}")
    
    return X_train, X_test, y_train, y_test

def train_model(X_train, y_train):
    """
    Train an IMPROVED Random Forest model
    """
    logger.info("🎯 Training Random Forest model...")
    
    # BETTER HYPERPARAMETERS:
    model = RandomForestRegressor(
        n_estimators=200,           # More trees
        max_depth=15,               # Deeper trees
        min_samples_split=5,        # Prevent overfitting
        min_samples_leaf=2,         # Prevent overfitting
        max_features='sqrt',        # Better for high-dimensional data
        bootstrap=True,
        random_state=42,
        n_jobs=-1,
        verbose=0
    )
    
    logger.info("⏳ Training started... (this may take a minute)")
    model.fit(X_train, y_train)
    logger.info("✅ Model training complete!")
    
    return model

def evaluate_model(model, X_test, y_test):
    """
    Evaluate model performance
    """
    logger.info("📊 Evaluating model...")
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mse)
    
    # Calculate percentage error
    y_mean = np.mean(y_test)
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    
    logger.info("=" * 40)
    logger.info("MODEL PERFORMANCE METRICS")
    logger.info("=" * 40)
    logger.info(f"📈 R² Score: {r2:.4f}")
    logger.info(f"📉 Mean Squared Error: {mse:.4f}")
    logger.info(f"📉 Root Mean Squared Error: {rmse:.4f}")
    logger.info(f"📉 Mean Absolute Error: {mae:.4f}")
    logger.info(f"📉 Mean Absolute % Error: {mape:.2f}%")
    logger.info(f"📊 Average house price: ${y_mean:.2f}k")
    
    return {
        'mse': float(mse),
        'rmse': float(rmse),
        'mae': float(mae),
        'r2': float(r2),
        'mape': float(mape),
        'y_mean': float(y_mean)
    }

def save_model(model, metrics):
    """
    Save model and metrics
    """
    logger.info("💾 Saving model and metrics...")
    
    # Create models directory
    os.makedirs("models", exist_ok=True)
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save model with timestamp
    model_filename = f"model_{timestamp}.pkl"
    model_path = f"models/{model_filename}"
    joblib.dump(model, model_path)
    
    # Save as latest model
    latest_path = "models/latest_model.pkl"
    joblib.dump(model, latest_path)
    
    # Add metadata to metrics
    metrics['timestamp'] = timestamp
    metrics['model_path'] = model_path
    metrics['model_type'] = str(type(model).__name__)
    
    # Save metrics
    metrics_path = f"models/metrics_{timestamp}.json"
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=4)
    
    # Save latest metrics
    latest_metrics_path = "models/latest_metrics.json"
    with open(latest_metrics_path, 'w') as f:
        json.dump(metrics, f, indent=4)
    
    logger.info(f"✅ Model saved: {model_path}")
    logger.info(f"✅ Metrics saved: {metrics_path}")
    
    return model_path, metrics_path

def plot_predictions(y_test, y_pred, save_path="models/predictions_plot.png"):
    """
    Create visualization of predictions vs actual
    """
    logger.info("📈 Creating prediction plot...")
    
    plt.figure(figsize=(10, 6))
    
    # Scatter plot
    plt.scatter(y_test, y_pred, alpha=0.5, label='Predictions')
    
    # Perfect prediction line
    max_val = max(y_test.max(), y_pred.max())
    min_val = min(y_test.min(), y_pred.min())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', label='Perfect Prediction')
    
    plt.xlabel('Actual Price ($1000s)')
    plt.ylabel('Predicted Price ($1000s)')
    plt.title('Actual vs Predicted House Prices')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Save plot
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=100, bbox_inches='tight')
    logger.info(f"📊 Plot saved: {save_path}")
    
    # Don't show plot in CLI environment
    plt.close()

def main():
    """Main training function"""
    print("=" * 50)
    print("STARTING MODEL TRAINING PIPELINE")
    print("=" * 50)
    
    # Load data
    X_train, X_test, y_train, y_test = load_processed_data()
    
    # Train model
    model = train_model(X_train, y_train)
    
    # Evaluate model
    metrics = evaluate_model(model, X_test, y_test)
    
    # Make predictions for plotting
    y_pred = model.predict(X_test)
    plot_predictions(y_test, y_pred)
    
    # Save everything
    model_path, metrics_path = save_model(model, metrics)
    
    print("\n" + "=" * 50)
    print("MODEL TRAINING COMPLETE!")
    print("=" * 50)
    print(f"Model saved: {model_path}")
    print(f"R² Score: {metrics['r2']:.4f}")
    print(f"RMSE: {metrics['rmse']:.4f}")
    
    return model, metrics

if __name__ == "__main__":
    model, metrics = main()