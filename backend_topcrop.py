from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)

@app.route('/top_crops', methods=['POST'])
def top_crops():
    try:
        data = request.json
        state = data.get("state")
        district = data.get("district")

        if not state or not district:
            return jsonify({"error": "State and District are required"}), 400

        result = subprocess.run(["Rscript", "topcrop.R", state, district], capture_output=True, text=True)
        
        output = json.loads(result.stdout)
        
        return jsonify(output)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8005)
