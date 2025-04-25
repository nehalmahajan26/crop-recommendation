from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import numpy as np
import tensorflow as tf
import pickle

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load TFLite model and allocate tensors
interpreter = tf.lite.Interpreter(model_path="crop_model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load scaler and label encoder
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)
with open('label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

def predict_crop(input_features):
    input_scaled = scaler.transform([input_features])
    interpreter.set_tensor(input_details[0]['index'], input_scaled.astype(np.float32))
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    predicted_index = np.argmax(output_data)
    predicted_crop = label_encoder.inverse_transform([predicted_index])
    return predicted_crop[0]

@app.route('/predict_crop', methods=['POST'])
def predict_crop_api():
    data = request.get_json()
    features = data.get("features")
    if features is None or len(features) != 7:
        return jsonify({"error": "Invalid input features. Provide 7 values."}), 400
    crop = predict_crop(features)
    return jsonify({"crop": crop})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
