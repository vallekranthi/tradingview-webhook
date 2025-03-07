from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# PickMyTrade Webhook URL
PICKMYTRADE_WEBHOOK_URL = "https://pickmytrade.trade/webhook"

# Your PickMyTrade API Token
PICKMYTRADE_API_TOKEN = "Ct8tPtD345345t3fty2EtYtCtVtVtUtL"

@app.route('/trade', methods=['POST'])
def trade():
    data = request.json  # Get data from TradingView

    if not data or "message" not in data:
        return jsonify({"error": "Invalid alert format"}), 400

    # Extract TradingView alert message
    alert_message = data["message"].strip().upper()  # Example: "BUY ES"

    # Split message to get action and symbol
    parts = alert_message.split(" ")
    if len(parts) < 2:
        return jsonify({"error": "Invalid alert format"}), 400

    action = parts[0].lower()  # "BUY" or "SELL"
    symbol = parts[1]  # Example: "ES"

    # Generate the PickMyTrade JSON payload
    pickmytrade_payload = {
        "symbol": symbol,
        "date": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "data": action,
        "quantity": "1",
        "risk_percentage": "0",
        "price": "0",  # Market order
        "tp": "0",
        "percentage_tp": "0",
        "dollar_tp": "2",
        "sl": "0",
        "dollar_sl": "0",
        "percentage_sl": "0",
        "trail": "0",
        "trail_stop": "0",
        "trail_trigger": "0",
        "trail_freq": "0",
        "update_tp": "false",
        "update_sl": "false",
        "token": PICKMYTRADE_API_TOKEN,
        "duplicate_position_allow": "true",
        "reverse_order_close": "true",
        "multiple_accounts": [
            {
                "token": "FtOtTt4345345tHkjhhiutTtUtAt1t8tTtDtG",
                "account_id": "2",
                "risk_percentage": 2,
                "quantity_multiplier": 0
            }
        ]
    }

    # Send the order to PickMyTrade
    response = requests.post(PICKMYTRADE_WEBHOOK_URL, json=pickmytrade_payload)

    return response.json()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
