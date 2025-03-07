from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# Your PickMyTrade Webhook URL
PICKMYTRADE_WEBHOOK_URL = "https://pickmytrade.trade/webhook"

# Your PickMyTrade API Token (Replace this with your actual token)
PICKMYTRADE_API_TOKEN = "Ct8tPtD345345t3fty2EtYtCtVtVtUtL"

@app.route('/trade', methods=['POST'])
def trade():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid data"}), 400
    
    # Extract TradingView alert details
    symbol = data.get("symbol")
    action = data.get("action")  # 'buy' or 'sell'
    quantity = str(data.get("quantity", 1))  # Convert to string if needed
    price = str(data.get("price", "0"))  # Closing price or market order
    
    # Construct PickMyTrade payload
    pickmytrade_payload = {
        "symbol": symbol,
        "date": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "data": action.lower(),  # 'buy' or 'sell'
        "quantity": quantity,
        "risk_percentage": "0",
        "price": price,
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
                "token": "FtOtTt4345345tHkjhhiutTtUtAt1t8tTtDtG",  # Replace with actual token
                "account_id": "2",
                "risk_percentage": 2,
                "quantity_multiplier": 0
            }
        ]
    }

    # Send request to PickMyTrade
    response = requests.post(PICKMYTRADE_WEBHOOK_URL, json=pickmytrade_payload)

    return response.json()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
