from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

EMISSION_RATE = 0.0023 # kg of CO2 saved per second of reduced idling



@app.route("/traffic", methods=["GET"])
def get_traffic():
    csv_path = 'traffic_log.csv'
    if not os.path.exists(csv_path):
        return jsonify({"vehicle_count": 0, "density": "Waiting...", "signal_time": 0})

    try:
        df = pd.read_csv(csv_path)
        if df.empty: return jsonify({"vehicle_count": 0})
        
        # Get latest count
        latest_count = int(df.iloc[-1, 1])

        # Dynamic Timing Logic
        if latest_count > 20:
            density, signal_time = "High", 90
        elif latest_count > 15:
            density, signal_time = "Medium", 60
        else:
            density, signal_time = "Low", 30

        # Calculation vs Fixed 90s timer
        idle_saved = 90 - signal_time
        emission_saved = round(idle_saved * EMISSION_RATE, 4)

        return jsonify({
            "vehicle_count": latest_count,
            "density": density,
            "signal_time": signal_time,
            "emission_saved": emission_saved
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)