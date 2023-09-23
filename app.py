from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)


@app.route("/get_stock_info", methods=["GET"])
def get_stock_info():
    ticker = request.args.get("ticker")

    if not ticker:
        return jsonify({"error": "Ticker symbol is required"}), 400

    try:
        stock = yf.Ticker(ticker)

        # Retrieve the latest values for EPS, PE ratio, and Price-to-Book ratio
        info = stock.info
        eps = info.get("trailingEps", None)  # Earnings per Share
        pe_ratio = info.get("trailingPE", None)  # Price-to-Earnings ratio
        pb_ratio = info.get("priceToBook", None)  # Price-to-Book ratio

        # Retrieve the latest dividends data
        # print(stock.dividends)
        # dividends = stock.dividends.tail(1).reset_index().to_dict(orient="records")

        result = {
            "ticker": ticker,
            "eps": eps,
            "pe_ratio": pe_ratio,
            "priceToBook": pb_ratio,
        }

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get_revenues", methods=["GET"])
def get_revenues():
    ticker = request.args.get("ticker")
    period = request.args.get("period", "3y")  # Default period is 3 years

    if not ticker:
        return jsonify({"error": "Ticker symbol is required"}), 400

    try:
        stock = yf.Ticker(ticker)

        # Fetch historical data for the specified period
        history = stock.history(period=period)
        print(history)

        n_years = int(period[:-1])  # Extract the number of years from the period

        # Calculate total revenue for each year
        total_revenues = [
            history.iloc[-n:]["Open"].sum() for n in range(1, n_years + 1)
        ]

        result = {
            "ticker": ticker,
            "total_revenues": total_revenues,
        }

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get_stock_price", methods=["GET"])
def get_stock_price():
    ticker = request.args.get("ticker")
    period = request.args.get("period", "1d")  # Default period is 1 day

    if not ticker:
        return jsonify({"error": "Ticker symbol is required"}), 400

    try:
        stock = yf.Ticker(ticker)

        # Fetch historical data for the specified period
        history = stock.history(period=period)

        # Extract date and closing price values
        price_data = history[["Open"]].reset_index()

        result = {
            "ticker": ticker,
            "period": period,
            "price_data": price_data.to_dict(orient="records"),
        }

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
