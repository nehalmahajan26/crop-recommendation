import requests

# Step 1: Predict crop
input_data = {
    "features": [90, 42, 43, 30, 25, 0, 0]  # Example input values
}
response = requests.post("http://host.docker.internal:5000/predict_crop", json=input_data)
predicted_crop = response.json().get("crop")
print("Recommended Crop:", predicted_crop)

# Step 2: Predict yield
yield_data = {
    "crop": predicted_crop,
    "Area": 10,
    "district": "ANANTAPUR"
}
response = requests.post("http://host.docker.internal:8002/predict_yield", json=yield_data)
yield_result = response.json()
print("Predicted Production:", yield_result.get("predicted_production"))
print("Yield (per hectare):", yield_result.get("yield"))
