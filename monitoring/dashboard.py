"""
Flask-based monitoring dashboard with Plotly charts.
Run with: python monitoring/dashboard.py
"""
from flask import Flask, render_template_string
import pandas as pd
import json
import os
import plotly.express as px
import plotly.utils
import plotly.graph_objects as go
import joblib

app = Flask(__name__)

# HTML template (embedded for simplicity)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>House Price Model Monitor</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body { font-family: Arial; margin: 20px; }
        .header { background-color: #4CAF50; color: white; padding: 10px; text-align: center; }
        .metrics { display: flex; gap: 20px; margin: 20px 0; }
        .metric-card { background: #f2f2f2; padding: 20px; border-radius: 5px; flex: 1; text-align: center; }
        .chart-container { margin-top: 30px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏠 House Price Prediction Monitoring</h1>
    </div>
    <div class="metrics">
        <div class="metric-card">
            <h3>R² Score</h3>
            <p>{{ r2 }}</p>
        </div>
        <div class="metric-card">
            <h3>RMSE</h3>
            <p>{{ rmse }}</p>
        </div>
        <div class="metric-card">
            <h3>MAE</h3>
            <p>{{ mae }}</p>
        </div>
        <div class="metric-card">
            <h3>MAPE</h3>
            <p>{{ mape }}%</p>
        </div>
    </div>
    <div class="chart-container">
        <div id="importance-chart"></div>
    </div>
    <script>
        var importanceGraph = {{ importance_graph | safe }};
        Plotly.newPlot('importance-chart', importanceGraph.data, importanceGraph.layout);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    # Load metrics
    metrics_path = "models/latest_metrics.json"
    if os.path.exists(metrics_path):
        with open(metrics_path, 'r') as f:
            metrics = json.load(f)
        r2 = f"{metrics.get('r2', 0):.4f}"
        rmse = f"{metrics.get('rmse', 0):.4f}"
        mae = f"{metrics.get('mae', 0):.4f}"
        mape = f"{metrics.get('mape', 0):.2f}"
    else:
        r2 = rmse = mae = mape = "N/A"

    # Feature importance
    model_path = "models/latest_model.pkl"
    if os.path.exists(model_path) and os.path.exists(metrics_path):
        model = joblib.load(model_path)
        if hasattr(model, 'feature_importances_'):
            feature_names = ["MedInc", "HouseAge", "AveRooms", "AveBedrms",
                             "Population", "AveOccup", "Latitude", "Longitude"]
            importances = model.feature_importances_
            df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
            df = df.sort_values('Importance', ascending=True)
            fig = px.bar(df, x='Importance', y='Feature', orientation='h',
                         title='Feature Importance', color='Importance',
                         color_continuous_scale='Blues')
            importance_graph = fig.to_json()
        else:
            importance_graph = None
    else:
        importance_graph = None

    return render_template_string(HTML_TEMPLATE,
                                  r2=r2,
                                  rmse=rmse,
                                  mae=mae,
                                  mape=mape,
                                  importance_graph=importance_graph)

if __name__ == '__main__':
    app.run(debug=True, port=8502)