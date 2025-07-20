from flask import Flask, render_template, jsonify
import requests
import json
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
        return render_template("index.html", data=data)
    except FileNotFoundError:
        return "No data available. Please visit /scrape to fetch data first."

@app.route("/scrape")
def scrape_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": False
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        coins = response.json()

        coin_data = []
        for coin in coins:
            coin_data.append({
                "name": coin["name"],
                "symbol": coin["symbol"].upper(),
                "price": coin["current_price"],
                "market_cap": coin["market_cap"],
                "rank": coin["market_cap_rank"],
                "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            })

        with open("data.json", "w") as f:
            json.dump(coin_data, f, indent=4)

        return jsonify({"message": "✅ Data scraped and saved to data.json", "data": coin_data})

    except Exception as e:
        return jsonify({"error": str(e)})
