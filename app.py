from flask import Flask, render_template, jsonify
import requests
import json
import os
from datetime import datetime

app = Flask(__name__)

def get_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": False
    }
    response = requests.get(url, params=params)
    data = response.json()

    # Add timestamp
    for coin in data:
        coin["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return data

@app.route("/")
def index():
    try:
        if not os.path.exists("data.json"):
            data = get_crypto_data()
            with open("data.json", "w") as f:
                json.dump(data, f)

        with open("data.json", "r") as f:
            try:
                crypto_data = json.load(f)
                if not isinstance(crypto_data, list):
                    raise ValueError("Invalid data format.")
            except Exception as e:
                print("Corrupted JSON, fetching fresh data:", e)
                crypto_data = get_crypto_data()
                with open("data.json", "w") as f_write:
                    json.dump(crypto_data, f_write)

        return render_template("index.html", crypto_data=crypto_data)

    except Exception as e:
        return f"An error occurred: {e}"

@app.route("/scrape")
def scrape():
    try:
        data = get_crypto_data()
        with open("data.json", "w") as f:
            json.dump(data, f)
        return jsonify({"message": "Data scraped and saved successfully."})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=False)
