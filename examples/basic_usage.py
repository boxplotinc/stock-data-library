from stocks.database import Database
from stocks.stocks import Stocks

def main():
    # Initialize the database and stocks manager
    db = Database('stocks.db')
    stocks_manager = Stocks(db)

    # Example usage: Add a ticker
    ticker = 'AAPL'
    stocks_manager.add_ticker(ticker)
    print(f"Added ticker: {ticker}")

    # Refresh data for all tickers
    stocks_manager.refresh_data()
    print("Refreshed data for all tickers.")

    # Example usage: Remove a ticker
    stocks_manager.remove_ticker(ticker)
    print(f"Removed ticker: {ticker}")

if __name__ == "__main__":
    main()