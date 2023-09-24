from flask import Flask, request, jsonify

app = Flask(__name__)

# Dictionary mapping ticker symbols to their total revenue values (a list of 5 values)
total_revenues_dict = {
    "AAPL": [294135000000, 265595000000, 260174000000, 247534000000, 215639000000],
    "TSLA": [31540000000, 24076000000, 21940000000, 21706500000, 11075400000],
    "GOOGL": [182527000000, 161857000000, 136819000000, 110855000000, 90119000000],
    "AMZN": [386064000000, 280522000000, 232887000000, 177866000000, 135987000000],
    "MSFT": [168088000000, 143015000000, 125843000000, 110360000000, 89953000000],
    "FB": [92903000000, 70400000000, 55838000000, 40653000000, 27638000000],
    "NVDA": [168144000000, 109181000000, 91118000000, 67893000000, 49710000000],
    "JPM": [115627000000, 106506000000, 105486000000, 111445000000, 95620000000],
    "WMT": [559151000000, 555188000000, 500343000000, 485873000000, 482130000000],
    # You can add more companies here
}

@app.route("/get_data", methods=["GET"])
def get_data():
    ticker = request.args.get("ticker")

    if not ticker:
        return jsonify({"error": "Ticker symbol is required"}), 400

    result = {"ticker": ticker}

    # Check if the ticker symbol exists in the dictionary
    if ticker in total_revenues_dict:
        revenues = total_revenues_dict[ticker]
        result["revenues"] = revenues
    else:
        return jsonify({"error": "Ticker symbol not found"}), 404

    # Realistic hardcoded values for stock price and stock info (replace with real values)
    stock_price = [
        {"Date": "2023-09-20", "Open": 150.0},
        {"Date": "2023-09-21", "Open": 155.0},
        {"Date": "2023-09-22", "Open": 160.0},
        # Add more data points as needed
    ]

    stock_info = {
        "eps": 4.51,
        "pe_ratio": 32.55,
        "priceToBook": 10.68,
        # Add more stock info data as needed
    }

    result["stock_price"] = stock_price
    result["stock_info"] = stock_info

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
