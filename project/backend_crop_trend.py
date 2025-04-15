from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json

app = Flask(__name__)
CORS(app)

@app.route('/crop_trend', methods=['POST'])
def crop_trend():
    data = request.get_json()
    crop = data.get("crop")
    if not crop:
        return jsonify({"error": "Crop name is required"}), 400
    try:
       
        cmd = ["Rscript", "crop_trend.R", crop]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return jsonify({"error": result.stderr}), 500
        output = json.loads(result.stdout)
        return jsonify(output)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8004) 
