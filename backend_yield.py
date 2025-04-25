from flask import Flask, request, jsonify
import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from flask_cors import CORS  

app = Flask(__name__)
CORS(app) 
with open('yield_model_xgb.pkl', 'rb') as f:
    model = pickle.load(f)
with open('scaler_xgb.pkl', 'rb') as f:
    scaler = pickle.load(f)
with open('ohe_columns.pkl', 'rb') as f:
    saved_columns = pickle.load(f)

@app.route('/predict_yield', methods=['POST'])
def predict_yield():
    try:
        data = request.get_json()
        print("Received Data:", data)  

        crop = data.get("crop", "rice").lower()
        area = float(data.get("Area"))
        crop_year = 2025  
        season = "Kharif"  

        input_df = pd.DataFrame([{ "Area": area, "Crop_Year": crop_year, "Crop": crop, "Season": season }])
        print("Input DataFrame:", input_df)  

        input_encoded = pd.get_dummies(input_df, columns=['Crop', 'Season'])
        for col in saved_columns:
            if col not in input_encoded.columns:
                input_encoded[col] = 0
        input_encoded = input_encoded[saved_columns]

        input_encoded[['Area', 'Crop_Year']] = scaler.transform(input_encoded[['Area', 'Crop_Year']])
        print("Encoded Input:", input_encoded)  

        log_predicted_production = model.predict(input_encoded)[0]
        predicted_production = float(np.exp(log_predicted_production)) 
        yield_per_ha = float(predicted_production / area)  

        print(f"Predicted Production: {predicted_production}, Yield: {yield_per_ha}")  

        return jsonify({
            "predicted_production": round(predicted_production, 2),
            "yield": round(yield_per_ha, 2)
        })
    except Exception as e:
        print("Error:", str(e))  
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=8002)
