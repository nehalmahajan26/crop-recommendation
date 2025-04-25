import requests

channel_id = "YOUR_CHANNEL_ID"
url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json?results=1"
response = requests.get(url)
data = response.json()
latest = data['feeds'][-1]

temperature = float(latest['field1'])
humidity = float(latest['field2'])
rainfall = float(latest['field3'])

# You enter N, P, K, pH manually
N, P, K, ph = 90, 40, 40, 6.5

features = [N, P, K, temperature, humidity, ph, rainfall]

api_url = "http://localhost:5000/predict_crop"
res = requests.post(api_url, json={"features": features})

if res.status_code == 200:
    print("✅ Recommended Crop:", res.json()["crop"])
else:
    print("❌ Error:", res.text)
