# Example of how to call the refresh_data method to update stock data for all tickers in the database.

from stocks.stocks import Stocks

def main():
    # Initialize the Stocks class
    stock_manager = Stocks()

    # Call the refresh_data method to update stock data
    stock_manager.refresh_data()

if __name__ == "__main__":
    main()