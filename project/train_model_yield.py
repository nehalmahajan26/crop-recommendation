import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import pickle

allowed_crops = [
    "banana", "blackgram", "coconut", "grapes", "jute", "lentil", "maize", "mango",
    "orange", "papaya", "rice", "jowar", "cashewnut", "sugarcane", "sweet potato", 
    "tapioca", "black pepper", "dry ginger", "arecanut", "dry chillies", "turmeric", 
    "urad", "bajra", "ragi", "groundnut", "wheat", "tobacco", "onion", "coriander", 
    "soyabean", "bhindi", "brinjal", "sesamum"
]

data = pd.read_csv('crop_production.csv')

data['Crop'] = data['Crop'].str.lower()
allowed_lower = [crop.lower() for crop in allowed_crops]
data = data[data['Crop'].isin(allowed_lower)]

data = data.dropna()
data = data[data['Production'] > 0]

data['log_Production'] = np.log(data['Production'])

features = ['Crop', 'Area', 'Crop_Year', 'Season']
target = 'log_Production'

X = pd.get_dummies(data[features], columns=['Crop', 'Season'])
y = data[target].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
cols_to_scale = ['Area', 'Crop_Year']
X_train[cols_to_scale] = scaler.fit_transform(X_train[cols_to_scale])
X_test[cols_to_scale] = scaler.transform(X_test[cols_to_scale])

model = XGBRegressor(
    n_estimators=1000,
    learning_rate=0.01,
    max_depth=5,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

model.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    verbose=True
)

y_pred_log = model.predict(X_test)
y_pred = np.exp(y_pred_log)
y_true = np.exp(y_test)

with open('yield_model_xgb.pkl', 'wb') as f:
    pickle.dump(model, f)
with open('scaler_xgb.pkl', 'wb') as f:
    pickle.dump(scaler, f)

with open('ohe_columns.pkl', 'wb') as f:
    pickle.dump(X.columns.tolist(), f)
print("Model and preprocessing objects saved.")


with open('yield_model_xgb.pkl', 'rb') as f:
    model_loaded = pickle.load(f)
with open('scaler_xgb.pkl', 'rb') as f:
    scaler_loaded = pickle.load(f)
with open('ohe_columns.pkl', 'rb') as f:
    saved_columns = pickle.load(f)
