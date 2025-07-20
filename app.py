from flask import Flask, render_template, jsonify
import requests
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
            return render_template('index.html', crypto_data=data)
    except Exception as e:
        print("Error loading data.json:", e)
        return render_template('index.html', crypto_data=None)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/scrape')
def scrape():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 10,
        'page': 1,
        'sparkline': 'false'
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise error for 4xx/5xx responses
        data = response.json()

        # Add timestamp
        for coin in data:
            coin['scraped_at'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

        with open('data.json', 'w') as file:
            json.dump(data, file, indent=2)

        return jsonify({"message": "Data scraped and saved successfully."})
    except requests.exceptions.HTTPError as e:
        return jsonify({"error": str(e)}), 429
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
