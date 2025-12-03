import pandas as pd
import numpy as np
import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  

# Load the dataset
df = joblib.load(r"C:\Users\HP845\Downloads\VASP\hybrid_dataset.pkl")

# Nearest Neighbor function
def nearest_neighbor(tds, flow):
    df_copy = df.copy()
    df_copy["distance"] = np.sqrt(
        (df_copy["Permeate_TDS"] - tds)**2 +
        (df_copy["Permeate_Flow"] - flow)**2
    )
    row = df_copy.loc[df_copy["distance"].idxmin()]
    return float(row["PX_Power_Savings"]), float(row["Power_Cost_Savings"])

# kNN Smoothing function
def knn_smoothing(tds, flow, k=5):
    df_copy = df.copy()
    df_copy["distance"] = np.sqrt(
        (df_copy["Permeate_TDS"] - tds)**2 +
        (df_copy["Permeate_Flow"] - flow)**2
    )
    nearest = df_copy.sort_values("distance").head(k)
    weights = 1 / (nearest["distance"] + 1e-6)
    px = np.average(nearest["PX_Power_Savings"], weights=weights)
    cost = np.average(nearest["Power_Cost_Savings"], weights=weights)
    return float(px), float(cost)

# Hybrid prediction 
def hybrid_predict(tds, flow, alpha=0.6):
    nn_px, nn_cost = nearest_neighbor(tds, flow)
    smooth_px, smooth_cost = knn_smoothing(tds, flow)
    final_px = alpha * nn_px + (1 - alpha) * smooth_px
    final_cost = alpha * nn_cost + (1 - alpha) * smooth_cost
    return {
        "final_prediction": {
            "px_power_savings": final_px,
            "power_cost_savings": final_cost
        },
        "nearest_neighbor": {
            "px_power_savings": nn_px,
            "power_cost_savings": nn_cost
        },
        "knn_smoothing": {
            "px_power_savings": smooth_px,
            "power_cost_savings": smooth_cost
        }
    }

# API endpoint 
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        tds = float(data['tds'])
        flow = float(data['flow'])
        
        result = hybrid_predict(tds, flow)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "API is running"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)