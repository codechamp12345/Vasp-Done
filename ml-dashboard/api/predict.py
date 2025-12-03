from http.server import BaseHTTPRequestHandler
import json
import pandas as pd
import numpy as np
import joblib
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Load the dataset
            pkl_paths = [
                os.path.join(os.path.dirname(__file__), 'hybrid_dataset.pkl'),
                os.path.join(os.path.dirname(__file__), '..', 'hybrid_dataset.pkl'),
                'hybrid_dataset.pkl'
            ]
            
            df = None
            for pkl_path in pkl_paths:
                if os.path.exists(pkl_path):
                    df = joblib.load(pkl_path)
                    break
            
            if df is None:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Dataset file not found"}).encode())
                return
            
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

            # Parse request body
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            tds = float(data.get('tds', 0))
            flow = float(data.get('flow', 0))
            
            result = hybrid_predict(tds, flow)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))
            
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
