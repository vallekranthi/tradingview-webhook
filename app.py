from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# PickMyTrade Webhook URL
PICKMYTRADE_WEBHOOK_URL = "https://api.pickmytrade.trade/v2/add-trade-data-latest"

# Your PickMyTrade API Token (Replace with actual token)
PICKMYTRADE_API_TOKEN = "Pwa489187f907f4a8bb141"

# Default Account Details (Replace with actual values)
ACCOUNT_ID = "PAAPEX2154810000003"

@app.route('/trade', methods=['POST'])
def trade():
    data = request.json  # Get TradingView alert data

    if not data or "message" not in data:
        return jsonify({"error": "Invalid alert format"}), 400

    # Extract TradingView alert message
    alert_message = data["message"].strip().upper()  # Example: "BUY MNQ1! 2 @ 15150"

    # Split message to get details (Example: "BUY MNQ1! 2 @ 15150")
    parts = alert_message.split(" ")
    if len(parts) < 3:
        return jsonify({"error": "Invalid alert format"}), 400

    action = parts[0].lower()  # "buy" or "sell"
    symbol = parts[1]  # Example: "MNQ1!"
    quantity = parts[2] if len(parts) > 2 else "1"  # Default to 1 if not provided
    price = parts[4] if "@" in parts else "0"  # Extract price if available

    # Map TradingView action to PickMyTrade format
    if action == "buy":
        trade_action = "long"
    elif action == "sell":
        trade_action = "short"
    else:
        return jsonify({"error": "Invalid action"}), 400

    # Construct PickMyTrade payload
    pickmytrade_payload = {
        "symbol": symbol,
        "date": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "data": trade_action,  # "long" for buy, "short" for sell
        "quantity": quantity,
        "risk_percentage": 0,
        "price": price,
        "tp": 0,
        "percentage_tp": 0,
        "dollar_tp": 25,
        "sl": 0,
        "dollar_sl": 25,
        "percentage_sl": 0,
        "trail": 0,
        "trail_stop": 0,
        "trail_trigger": 0,
        "trail_freq": 0,
        "update_tp": False,
        "update_sl": False,
        "breakeven": 0,
        "token": PICKMYTRADE_API_TOKEN,
        "pyramid": False,
        "reverse_order_close": True,
        "multiple_accounts": [
            {
                "token": PICKMYTRADE_API_TOKEN,
                "account_id": ACCOUNT_ID,
                "risk_percentage": 0,
                "quantity_multiplier": 1
            }
        ]
    }

    # Send trade request to PickMyTrade
    response = requests.post(PICKMYTRADE_WEBHOOK_URL, json=pickmytrade_payload)

    return response.json()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
