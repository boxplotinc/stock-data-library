from src.stocks.database import Database
from src.stocks.stocks import Stocks

def main():
    # Initialize the database and stocks manager
    db = Database('example_stocks.db')
    stocks_manager = Stocks(db.connection)

    print("\n1. Adding tickers with different date ranges")
    # Add a ticker with default date range (last 10 years)
    stocks_manager.add_ticker('AAPL')
    
    # Add a ticker with a specific date range
    stocks_manager.add_ticker('MSFT', '2020-01-01', '2023-12-31')
    
    # Print all tickers in the database
    tickers = stocks_manager.get_all_tickers()
    print(f"Tickers in database: {tickers}")
    
    print("\n2. Retrieving data with date filters")
    # Get all data for a ticker
    all_data = stocks_manager.get_ticker_data('AAPL')
    if all_data:
        print(f"Retrieved {len(all_data)} records for AAPL (all dates)")
        
    # Get data for a specific date range
    filtered_data = stocks_manager.get_ticker_data('MSFT', '2022-01-01', '2022-12-31')
    if filtered_data:
        print(f"Retrieved {len(filtered_data)} records for MSFT (2022 only)")
    
    print("\n3. Refreshing data for specific date ranges")
    # Refresh data for a specific historical period
    stocks_manager.refresh_data('2018-01-01', '2018-12-31')
    
    print("\n4. Refreshing news")
    stocks_manager.refresh_news()
    
    news = stocks_manager.get_ticker_news('AAPL')
    if news:
        print(f"Retrieved {len(news)} news items for AAPL")
        print(f"Most recent news: {news[0][3][:100]}...")
    
    print("\n5. Removing a ticker")
    stocks_manager.remove_ticker('MSFT')
    remaining_tickers = stocks_manager.get_all_tickers()
    print(f"Remaining tickers: {remaining_tickers}")
    
    # Close database connection
    db.close()

if __name__ == "__main__":
    main()