# Example of how to use the enhanced refresh_data methods with date parameters

from src.stocks.database import Database
from src.stocks.stocks import Stocks
from datetime import datetime, timedelta

def main():
    # Initialize the database and stocks manager
    db = Database('example_stocks.db')
    stocks_manager = Stocks(db.connection)
    
    # Add some tickers if they don't exist
    tickers_to_add = ['AAPL', 'MSFT', 'GOOGL']
    for ticker in tickers_to_add:
        stocks_manager.add_ticker(ticker)
    
    print("\nExample 1: Refresh for a specific date range (last month)")
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)
    stocks_manager.refresh_data(start_date, end_date)
    
    print("\nExample 2: Refresh for specific calendar year")
    stocks_manager.refresh_data('2023-01-01', '2023-12-31')
    
    print("\nExample 3: Refresh for a specific ticker with date range")
    stocks_manager.refresh_data_for_ticker('AAPL', '2022-01-01', '2022-06-30')
    
    print("\nExample 4: Refresh for a specific ticker without date range (default behavior)")
    stocks_manager.refresh_data_for_ticker('GOOGL')
    
    print("\nExample 5: Query data with date filters")
    # Get data for all of 2023
    data_2023 = stocks_manager.get_ticker_data('AAPL', '2023-01-01', '2023-12-31')
    print(f"Retrieved {len(data_2023)} data points for AAPL in 2023")
    
    # Get data since a specific date
    data_since = stocks_manager.get_ticker_data('MSFT', '2023-06-01')
    print(f"Retrieved {len(data_since)} data points for MSFT since June 1, 2023")
    
    # Get data until a specific date
    data_until = stocks_manager.get_ticker_data('GOOGL', end_date='2023-12-31')
    print(f"Retrieved {len(data_until)} data points for GOOGL until Dec 31, 2023")
    
    # Close database connection
    db.close()

if __name__ == "__main__":
    main()