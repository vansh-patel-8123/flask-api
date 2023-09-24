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
    "AMZN": [
        {"year": 2023, "revenue": 56789000000},
        {"year": 2022, "revenue": 38622000000},
        {"year": 2021, "revenue": 38622000000},
        {"year": 2020, "revenue": 38622000000},
        {"year": 2019, "revenue": 38622000000},
    ],
    "MSFT": [
        {"year": 2023, "revenue": 200000000000},
        {"year": 2022, "revenue": 169559000000},
        {"year": 2021, "revenue": 169559000000},
        {"year": 2020, "revenue": 169559000000},
        {"year": 2019, "revenue": 169559000000},
    ],
    "FB": [
        {"year": 2023, "revenue": 12345000000},
        {"year": 2022, "revenue": 9876000000},
        {"year": 2021, "revenue": 8765000000},
        {"year": 2020, "revenue": 7654000000},
        {"year": 2019, "revenue": 6543000000},
    ],
    "NFLX": [
        {"year": 2023, "revenue": 30000000000},
        {"year": 2022, "revenue": 27000000000},
        {"year": 2021, "revenue": 24000000000},
        {"year": 2020, "revenue": 21000000000},
        {"year": 2019, "revenue": 18000000000},
    ],
    "NVDA": [
        {"year": 2023, "revenue": 21000000000},
        {"year": 2022, "revenue": 18000000000},
        {"year": 2021, "revenue": 15000000000},
        {"year": 2020, "revenue": 12000000000},
        {"year": 2019, "revenue": 9000000000},
    ],
    "GOOG": [
        {"year": 2023, "revenue": 200000000000},
        {"year": 2022, "revenue": 180000000000},
        {"year": 2021, "revenue": 160000000000},
        {"year": 2020, "revenue": 140000000000},
        {"year": 2019, "revenue": 120000000000},
    ],
    "IBM": [
        {"year": 2023, "revenue": 56000000000},
        {"year": 2022, "revenue": 54000000000},
        {"year": 2021, "revenue": 52000000000},
        {"year": 2020, "revenue": 50000000000},
        {"year": 2019, "revenue": 48000000000},
    ],
}


stock_info_dict = {
    "AAPL": {"eps": 4.51, "pe_ratio": 32.55, "priceToBook": 10.68},
    "TSLA": {"eps": 0.01, "pe_ratio": 123.45, "priceToBook": 56.78},
    "GOOGL": {"eps": 29.73, "pe_ratio": 28.12, "priceToBook": 6.54},
    "AMZN": {"eps": 40.56, "pe_ratio": 64.78, "priceToBook": 9.43},
    "MSFT": {"eps": 5.32, "pe_ratio": 31.47, "priceToBook": 13.62},
    "FB": {"eps": 3.45, "pe_ratio": 25.67, "priceToBook": 8.91},
    "NFLX": {"eps": 2.34, "pe_ratio": 45.89, "priceToBook": 11.76},
    "NVDA": {"eps": 3.67, "pe_ratio": 56.78, "priceToBook": 14.32},
    "GOOG": {"eps": 7.89, "pe_ratio": 31.23, "priceToBook": 7.45},
    "IBM": {"eps": 4.56, "pe_ratio": 20.34, "priceToBook": 5.67},
}

latest_stock_price_dict = {
    "AAPL": 150.0,
    "TSLA": 750.0,
    "GOOGL": 2800.0,
    "AMZN": 3500.0,
    "MSFT": 300.0,
    "FB": 350.0,
    "NFLX": 600.0,
    "NVDA": 250.0,
    "GOOG": 2750.0,
    "IBM": 140.0,
}

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
    "GOOGL": [
        {"Date": "2023-09-20", "Open": 2800.0},
        {"Date": "2023-09-21", "Open": 2805.0},
        {"Date": "2023-09-22", "Open": 2810.0},
        {"Date": "2023-09-23", "Open": 2808.0},
        {"Date": "2023-09-24", "Open": 2812.5},
        {"Date": "2023-09-27", "Open": 2805.0},
        {"Date": "2023-09-28", "Open": 2810.0},
        {"Date": "2023-09-29", "Open": 2809.0},
        {"Date": "2023-09-30", "Open": 2811.0},
        {"Date": "2023-10-01", "Open": 2812.0},
    ],
    "AMZN": [
        {"Date": "2023-09-20", "Open": 3500.0},
        {"Date": "2023-09-21", "Open": 3550.0},
        {"Date": "2023-09-22", "Open": 3600.0},
        {"Date": "2023-09-23", "Open": 3580.0},
        {"Date": "2023-09-24", "Open": 3590.5},
        {"Date": "2023-09-27", "Open": 3575.0},
        {"Date": "2023-09-28", "Open": 3590.0},
        {"Date": "2023-09-29", "Open": 3595.0},
        {"Date": "2023-09-30", "Open": 3600.0},
        {"Date": "2023-10-01", "Open": 3610.0},
    ],
    "MSFT": [
        {"Date": "2023-09-20", "Open": 300.0},
        {"Date": "2023-09-21", "Open": 305.0},
        {"Date": "2023-09-22", "Open": 310.0},
        {"Date": "2023-09-23", "Open": 308.0},
        {"Date": "2023-09-24", "Open": 309.5},
        {"Date": "2023-09-27", "Open": 307.0},
        {"Date": "2023-09-28", "Open": 308.5},
        {"Date": "2023-09-29", "Open": 307.5},
        {"Date": "2023-09-30", "Open": 309.0},
        {"Date": "2023-10-01", "Open": 310.0},
    ],
    "FB": [
        {"Date": "2023-09-20", "Open": 350.0},
        {"Date": "2023-09-21", "Open": 355.0},
        {"Date": "2023-09-22", "Open": 360.0},
        {"Date": "2023-09-23", "Open": 358.0},
        {"Date": "2023-09-24", "Open": 359.5},
        {"Date": "2023-09-27", "Open": 357.0},
        {"Date": "2023-09-28", "Open": 359.0},
        {"Date": "2023-09-29", "Open": 359.5},
        {"Date": "2023-09-30", "Open": 360.0},
        {"Date": "2023-10-01", "Open": 361.0},
    ],
    "NFLX": [
        {"Date": "2023-09-20", "Open": 600.0},
        {"Date": "2023-09-21", "Open": 605.0},
        {"Date": "2023-09-22", "Open": 610.0},
        {"Date": "2023-09-23", "Open": 608.0},
        {"Date": "2023-09-24", "Open": 609.5},
        {"Date": "2023-09-27", "Open": 607.0},
        {"Date": "2023-09-28", "Open": 609.0},
        {"Date": "2023-09-29", "Open": 609.5},
        {"Date": "2023-09-30", "Open": 610.0},
        {"Date": "2023-10-01", "Open": 611.0},
    ],
    "NVDA": [
        {"Date": "2023-09-20", "Open": 250.0},
        {"Date": "2023-09-21", "Open": 255.0},
        {"Date": "2023-09-22", "Open": 260.0},
        {"Date": "2023-09-23", "Open": 258.0},
        {"Date": "2023-09-24", "Open": 259.5},
        {"Date": "2023-09-27", "Open": 257.0},
        {"Date": "2023-09-28", "Open": 259.0},
        {"Date": "2023-09-29", "Open": 259.5},
        {"Date": "2023-09-30", "Open": 260.0},
        {"Date": "2023-10-01", "Open": 261.0},
    ],
    "GOOG": [
        {"Date": "2023-09-20", "Open": 2750.0},
        {"Date": "2023-09-21", "Open": 2755.0},
        {"Date": "2023-09-22", "Open": 2760.0},
        {"Date": "2023-09-23", "Open": 2758.0},
        {"Date": "2023-09-24", "Open": 2760.5},
        {"Date": "2023-09-27", "Open": 2760.0},
        {"Date": "2023-09-28", "Open": 2761.0},
        {"Date": "2023-09-29", "Open": 2762.0},
        {"Date": "2023-09-30", "Open": 2765.0},
        {"Date": "2023-10-01", "Open": 2766.0},
    ],
    "IBM": [
        {"Date": "2023-09-20", "Open": 140.0},
        {"Date": "2023-09-21", "Open": 141.0},
        {"Date": "2023-09-22", "Open": 142.0},
        {"Date": "2023-09-23", "Open": 141.5},
        {"Date": "2023-09-24", "Open": 142.5},
        {"Date": "2023-09-27", "Open": 142.0},
        {"Date": "2023-09-28", "Open": 143.0},
        {"Date": "2023-09-29", "Open": 144.0},
        {"Date": "2023-09-30", "Open": 143.5},
        {"Date": "2023-10-01", "Open": 144.5},
    ],
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
