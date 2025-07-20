from flask import Flask, render_template, jsonify
import requests
import json
import time
import os

app = Flask(__name__)

DATA_FILE = 'data.json'

def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": "10",
        "page": "1",
        "sparkline": "false"
    }

    for attempt in range(3):  # Try 3 times if rate limit hit
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print(f"[Rate Limit] Attempt {attempt+1}: Waiting 10 seconds...")
            time.sleep(10)
        else:
            response.raise_for_status()

    raise Exception("Failed to fetch data after retries.")

@app.route('/')
def index():
    if not os.path.exists(DATA_FILE):
        return "No data available. Please visit /scrape first.", 404

    with open(DATA_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return "Data file is corrupted or empty.", 500

    return render_template('index.html', coins=data)

@app.route('/scrape')
def scrape():
    try:
        data = fetch_crypto_data()
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        return jsonify({"message": "Data scraped and saved successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

