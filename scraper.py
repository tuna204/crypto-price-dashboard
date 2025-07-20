import requests
import json
import datetime

def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": "false"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        crypto_data = []
        for coin in data:
            crypto_data.append({
                "name": coin["name"],
                "symbol": coin["symbol"].upper(),
                "price": f"${coin['current_price']:,.2f}",
                "market_cap": f"${coin['market_cap']:,.0f}",
                "last_updated": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            })

        with open("data.json", "w") as f:
            json.dump(crypto_data, f, indent=4)

        print("✅ Data saved to data.json")

    except Exception as e:
        print("❌ Error fetching data:", e)

if __name__ == "__main__":
    fetch_crypto_data()
