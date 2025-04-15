import os
import sys
import json
import time
import random
import threading
from flask import Flask, render_template, jsonify
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, FloatType, IntegerType
from pyspark.sql.functions import col

# --- Spark Setup ---
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

app = Flask(__name__)

# Initialize Spark session
spark = SparkSession.builder \
    .appName("AgriSparkBatchSim") \
    .master("local[*]") \
    .getOrCreate()

# Directory to store simulated data
DATA_DIR = "sim_data"
os.makedirs(DATA_DIR, exist_ok=True)

# --- Simulated Data Generator ---
def simulate_data():
    while True:
        record = {
            "N": random.randint(0, 140),
            "P": random.randint(5, 145),
            "K": random.randint(5, 205),
            "temperature": round(random.uniform(10, 40), 2),
            "humidity": round(random.uniform(10, 90), 2),
            "ph": round(random.uniform(4.0, 9.0), 2),
            "rainfall": round(random.uniform(20.0, 300.0), 2),
            "timestamp": int(time.time())
        }
        filename = os.path.join(DATA_DIR, f"data_{time.time()}.json")
        with open(filename, "w") as f:
            json.dump(record, f)
        time.sleep(2)

# Run the data simulation in a separate thread
threading.Thread(target=simulate_data, daemon=True).start()

# --- Define Schema for Spark Data ---
schema = StructType([
    StructField("N", IntegerType(), True),
    StructField("P", IntegerType(), True),
    StructField("K", IntegerType(), True),
    StructField("temperature", FloatType(), True),
    StructField("humidity", FloatType(), True),
    StructField("ph", FloatType(), True),
    StructField("rainfall", FloatType(), True),
    StructField("timestamp", IntegerType(), True)
])

# --- Flask Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/spark-data')
def get_data():
    # Read all available files as batch
    df = spark.read.schema(schema).json(DATA_DIR)
    df.createOrReplaceTempView("agri_data")

    # Calculate averages
    avg_df = spark.sql("""
        SELECT 
            ROUND(AVG(N), 2) as avg_N,
            ROUND(AVG(P), 2) as avg_P,
            ROUND(AVG(K), 2) as avg_K,
            ROUND(AVG(temperature), 2) as avg_temp,
            ROUND(AVG(humidity), 2) as avg_humidity,
            ROUND(AVG(ph), 2) as avg_ph,
            ROUND(AVG(rainfall), 2) as avg_rain
        FROM agri_data
    """)
    averages = avg_df.collect()[0].asDict()

    # Get the latest 10 records
    latest_df = spark.sql("SELECT * FROM agri_data ORDER BY timestamp DESC LIMIT 10")
    latest_data = latest_df.toPandas().to_dict(orient="records")

    return jsonify({
        "averages": averages,
        "latest_data": latest_data
    })

@app.route('/stream')
def stream_page():
    return render_template('spark_streaming.html')

if __name__ == '__main__':
    app.run(debug=True, port=5050)
