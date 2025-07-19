from flask import Flask, render_template
import requests

app = Flask(__name__)

def get_crypto_data():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 10,
            'page': 1,
            'sparkline': False
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching crypto data: {e}")
        return None

@app.route('/')
def index():
    crypto_data = get_crypto_data()
    return render_template("index.html", crypto_data=crypto_data)

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=False)

