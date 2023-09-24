from flask import Flask, request, jsonify

app = Flask(__name__)

# Dictionary mapping ticker symbols to their total revenue values (a list of dictionaries with year and revenue)
total_revenues_dict = {
    "AAPL": [
        {"year": 2023, "revenue": 294135000000},
        {"year": 2022, "revenue": 265595000000},
        {"year": 2021, "revenue": 260174000000},
        {"year": 2020, "revenue": 247534000000},
        {"year": 2019, "revenue": 215639000000},
    ],
    "TSLA": [
        {"year": 2023, "revenue": 31540000000},
        {"year": 2022, "revenue": 24076000000},
        {"year": 2021, "revenue": 21940000000},
        {"year": 2020, "revenue": 21706500000},
        {"year": 2019, "revenue": 11075400000},
    ],
    "GOOGL": [
        {"year": 2023, "revenue": 182527000000},
        {"year": 2022, "revenue": 161857000000},
        {"year": 2021, "revenue": 136819000000},
        {"year": 2020, "revenue": 110855000000},
        {"year": 2019, "revenue": 90119000000},
    ],
    # Add more companies with year and revenue data here
}

# Dictionary mapping ticker symbols to their stock info
stock_info_dict = {
    "AAPL": {"eps": 4.51, "pe_ratio": 32.55, "priceToBook": 10.68},
    "TSLA": {"eps": 0.01, "pe_ratio": 123.45, "priceToBook": 56.78},
    "GOOGL": {"eps": 29.73, "pe_ratio": 28.12, "priceToBook": 6.54},
    # Add more stock info data as needed for additional companies
}

# Dictionary mapping ticker symbols to their latest stock price (realistic hardcoded values)
latest_stock_price_dict = {
    "AAPL": 150.0,
    "TSLA": 750.0,
    "GOOGL": 2800.0,
    # Add more latest stock prices here
}

# Realistic hardcoded values for stock price (10 data points)
stock_price_dict = {
    "AAPL": [
        {"Date": "2023-09-20", "Open": 150.0},
        {"Date": "2023-09-21", "Open": 155.0},
        {"Date": "2023-09-22", "Open": 160.0},
        {"Date": "2023-09-23", "Open": 158.0},
        {"Date": "2023-09-24", "Open": 157.5},
        {"Date": "2023-09-27", "Open": 159.0},
        {"Date": "2023-09-28", "Open": 161.0},
        {"Date": "2023-09-29", "Open": 162.0},
        {"Date": "2023-09-30", "Open": 165.0},
        {"Date": "2023-10-01", "Open": 166.0},
    ],
    "TSLA": [
        {"Date": "2023-09-20", "Open": 750.0},
        {"Date": "2023-09-21", "Open": 755.0},
        {"Date": "2023-09-22", "Open": 760.0},
        {"Date": "2023-09-23", "Open": 758.0},
        {"Date": "2023-09-24", "Open": 757.5},
        {"Date": "2023-09-27", "Open": 759.0},
        {"Date": "2023-09-28", "Open": 761.0},
        {"Date": "2023-09-29", "Open": 762.0},
        {"Date": "2023-09-30", "Open": 765.0},
        {"Date": "2023-10-01", "Open": 766.0},
    ],
    # Add more stock price data for other companies here
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

    # Fetch the latest stock price from the dictionary
    if ticker in latest_stock_price_dict:
        latest_price = latest_stock_price_dict[ticker]
        result["baseValue"] = latest_price

    # Retrieve stock info from the dictionary
    if ticker in stock_info_dict:
        stock_info = stock_info_dict[ticker]
        result["stock_info"] = stock_info

    # Add the list of stock prices to the response
    if ticker in stock_price_dict:
        stock_prices = stock_price_dict[ticker]
        result["stock_price"] = stock_prices

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
