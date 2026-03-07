"""
Simple monitoring dashboard using Streamlit.
Displays model metrics, feature importance, and recent predictions.
Run with: streamlit run monitoring/simple_dashboard.py
"""
import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import joblib
import matplotlib.pyplot as plt
from datetime import datetime

# Page config
st.set_page_config(page_title="House Price Model Monitor", layout="wide")
st.title("🏠 House Price Prediction - Model Monitoring Dashboard")

# Sidebar for navigation
st.sidebar.header("Navigation")
option = st.sidebar.radio("Go to", ["Model Performance", "Feature Importance", "Recent Predictions"])

# Load latest metrics
metrics_path = "models/latest_metrics.json"
if os.path.exists(metrics_path):
    with open(metrics_path, 'r') as f:
        metrics = json.load(f)
    model_version = metrics.get('timestamp', 'unknown')
else:
    metrics = None
    model_version = 'N/A'

# Load model for feature importance (if available)
model = None
model_path = "models/latest_model.pkl"
if os.path.exists(model_path):
    model = joblib.load(model_path)

# 1. Model Performance Page
if option == "Model Performance":
    st.header("📊 Model Performance Metrics")
    if metrics:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("R² Score", f"{metrics.get('r2', 0):.4f}")
        col2.metric("RMSE", f"{metrics.get('rmse', 0):.4f}")
        col3.metric("MAE", f"{metrics.get('mae', 0):.4f}")
        col4.metric("MAPE", f"{metrics.get('mape', 0):.2f}%")
        
        st.write(f"**Model Version:** {model_version}")
        st.write(f"**Training Date:** {metrics.get('timestamp', 'N/A')}")
        
        # Display the actual vs predicted plot if exists
        plot_path = "models/predictions_plot.png"
        if os.path.exists(plot_path):
            st.image(plot_path, caption="Actual vs Predicted (Test Set)")
    else:
        st.warning("No metrics found. Train a model first.")

# 2. Feature Importance Page
elif option == "Feature Importance":
    st.header("🔍 Feature Importance")
    if model and hasattr(model, 'feature_importances_'):
        # Get feature names (hardcoded for this dataset)
        feature_names = ["MedInc", "HouseAge", "AveRooms", "AveBedrms",
                         "Population", "AveOccup", "Latitude", "Longitude"]
        importances = model.feature_importances_
        
        # Create DataFrame
        feat_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': importances
        }).sort_values('Importance', ascending=False)
        
        # Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(feat_df['Feature'], feat_df['Importance'], color='skyblue')
        ax.set_xlabel('Importance')
        ax.set_title('Random Forest Feature Importance')
        st.pyplot(fig)
    else:
        st.warning("Model does not provide feature importances or not loaded.")

# 3. Recent Predictions Page
elif option == "Recent Predictions":
    st.header("📈 Recent Predictions Log")
    # Check if prediction log exists (optional, we can simulate or read from a CSV)
    log_path = "logs/predictions.csv"
    if os.path.exists(log_path):
        df = pd.read_csv(log_path)
        st.dataframe(df.tail(20))
        
        # Plot prediction trend
        if len(df) > 1:
            fig, ax = plt.subplots()
            ax.plot(pd.to_datetime(df['timestamp']), df['predicted_price'], marker='o', linestyle='-')
            ax.set_xlabel('Time')
            ax.set_ylabel('Predicted Price ($)')
            ax.set_title('Prediction Trend')
            plt.xticks(rotation=45)
            st.pyplot(fig)
    else:
        st.info("No prediction log found. To enable logging, modify your API to append predictions to `logs/predictions.csv`.")
        # Show a sample table for demonstration
        sample_data = {
            'timestamp': [datetime.now().isoformat()] * 3,
            'predicted_price': [450000, 520000, 480000],
            'actual_price': [None, None, None]  # if you log actuals later
        }
        st.write("Example of what the log could look like:")
        st.dataframe(pd.DataFrame(sample_data))