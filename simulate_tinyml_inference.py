
import numpy as np
import tensorflow as tf
import pickle

interpreter = tf.lite.Interpreter(model_path="crop_model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

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

sample_input = [90, 42, 43, 20.87, 82.00, 6.5, 202.93] 
print("Recommended Crop:", predict_crop(sample_input))