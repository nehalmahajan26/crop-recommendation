import pandas as pd
import numpy as np
import pickle
from xgboost import XGBRegressor

df = pd.read_csv("crop_production.csv")
df.columns = df.columns.str.strip() 

allowed_crops = [
     "banana", "blackgram", "coconut", "grapes", "jute", "lentil", "maize", "mango",
    "orange", "papaya", "rice", "jowar", "cashewnut", "sugarcane", "sweet potato", 
    "tapioca", "black pepper", "dry ginger", "arecanut", "dry chillies", "turmeric", 
    "urad", "bajra", "ragi", "groundnut", "wheat", "tobacco", "onion", "coriander", 
    "soyabean", "bhindi", "brinjal", "sesamum"
]

df = df[df["Crop"].str.lower().isin(allowed_crops)].copy()
df = df[["District_Name", "Crop", "Season", "Area", "Crop_Year", "Production"]].dropna()

df["Area"] = pd.to_numeric(df["Area"], errors="coerce")
df["Crop_Year"] = pd.to_numeric(df["Crop_Year"], errors="coerce")
df["Production"] = pd.to_numeric(df["Production"], errors="coerce")
df.dropna(inplace=True)

df = df[df["Production"] > 0]

df["log_Production"] = np.log(df["Production"])


with open("yield_model_xgb.pkl", "rb") as f:
    model = pickle.load(f)
with open("scaler_xgb.pkl", "rb") as f:
    scaler = pickle.load(f)
with open("ohe_columns.pkl", "rb") as f:
    saved_columns = pickle.load(f)

df_encoded = pd.get_dummies(df, columns=["Crop", "Season"])

for col in saved_columns:
    if col not in df_encoded.columns:
        df_encoded[col] = 0
df_encoded = df_encoded[saved_columns]

df_encoded[["Area", "Crop_Year"]] = scaler.transform(df_encoded[["Area", "Crop_Year"]])

log_predicted_production = model.predict(df_encoded)
predicted_production = np.exp(log_predicted_production) 

predicted_production = np.maximum(predicted_production, 0)

df["Predicted_Production"] = predicted_production
df["Predicted_Yield"] = (df["Predicted_Production"] / df["Area"]).clip(lower=0)  


df.drop(columns=["log_Production"], inplace=True) 
df.to_csv("predicted_yield_xgb.csv", index=False)

print("Predicted yield data saved to `predicted_yield_xgb.csv` correctly!")
