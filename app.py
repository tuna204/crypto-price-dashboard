from flask import Flask, render_template
import requests, time

app = Flask(__name__)

cached_data = []
last_fetch_time = 0
FETCH_INTERVAL = 60 * 60  # 1 hour

def get_crypto_data():
    global cached_data, last_fetch_time
    now = time.time()
    if now - last_fetch_time > FETCH_INTERVAL:
        try:
            url = "https://api.coingecko.com/api/v3/coins/markets"
            params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 10, "page": 1, "sparkline": False}
            response = requests.get(url, params=params)
            response.raise_for_status()
            cached_data = response.json()
            last_fetch_time = now
        except Exception as e:
            print(f"Error fetching crypto data: {e}")
    return cached_data

@app.route("/")
def index():
    data = get_crypto_data()
    return render_template("index.html", data=data)

@app.route("/about")
def about():
    return render_template("about.html")
