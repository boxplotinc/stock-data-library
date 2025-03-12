import sys
import os
from datetime import datetime, timedelta

# Get the absolute path of the src directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
from stocks.stocks import Stocks
from stocks.database import Database

class TestStocks(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = Database('test_stocks.db')
        cls.stocks = Stocks(cls.db.connection)
        
        # Add test ticker that will be used across tests
        cls.stocks.add_ticker('AAPL')

    def test_add_ticker(self):
        self.stocks.add_ticker('TSLA')  # Using a different ticker to avoid conflicts
        tickers = self.stocks.get_all_tickers()
        self.assertIn('TSLA', tickers)

    def test_add_ticker_with_date_range(self):
        # Test adding ticker with specific date range
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=60)  # Last 60 days
        
        self.stocks.add_ticker('AMD', start_date, end_date)
        data = self.stocks.get_ticker_data('AMD', start_date, end_date)
        self.assertIsNotNone(data)
        self.assertTrue(len(data) > 0, "Should have fetched data within the date range")

    def test_remove_ticker(self):
        self.stocks.add_ticker('GOOGL')
        self.stocks.remove_ticker('GOOGL')
        tickers = self.stocks.get_all_tickers()
        self.assertNotIn('GOOGL', tickers)

    def test_refresh_data(self):
        self.stocks.add_ticker('MSFT')
        self.stocks.refresh_data()
        data = self.stocks.get_ticker_data('MSFT')
        self.assertIsNotNone(data)
        self.assertTrue(len(data) > 0, "Should have fetched at least some data")

    def test_refresh_data_with_date_range(self):
        # Test refreshing with specific date range
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)  # Last 30 days
        
        self.stocks.refresh_data_for_ticker('AAPL', start_date, end_date)
        
        # Get data and verify it's within the specified range
        data = self.stocks.get_ticker_data('AAPL', start_date, end_date)
        
        self.assertIsNotNone(data)
        self.assertTrue(len(data) > 0, "Should have fetched data within the date range")
        
        # Convert date strings to datetime objects for comparison
        if data:
            data_dates = [datetime.strptime(row[1], '%Y-%m-%d').date() for row in data]
            self.assertTrue(all(start_date <= date <= end_date for date in data_dates), 
                           "All dates should be within the specified range")

    def test_get_ticker_data_with_date_range(self):
        # First ensure we have some data
        self.stocks.refresh_data_for_ticker('AAPL')
        
        # Define date range
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=60)  # Last 60 days
        
        # Test with string dates
        data1 = self.stocks.get_ticker_data('AAPL', start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        
        # Test with datetime objects
        data2 = self.stocks.get_ticker_data('AAPL', start_date, end_date)
        
        # Verify results
        self.assertEqual(len(data1), len(data2), "Both query methods should return same number of results")
        
        # Test with only start date
        data3 = self.stocks.get_ticker_data('AAPL', start_date=start_date)
        self.assertIsNotNone(data3)
        
        # Test with only end date
        data4 = self.stocks.get_ticker_data('AAPL', end_date=end_date)
        self.assertIsNotNone(data4)
        
        # Verify date order (descending)
        if len(data1) > 1:
            date1 = datetime.strptime(data1[0][1], '%Y-%m-%d').date()
            date2 = datetime.strptime(data1[1][1], '%Y-%m-%d').date()
            self.assertGreaterEqual(date1, date2, "Dates should be in descending order")

    def test_refresh_news(self):
        self.stocks.add_ticker('TSLA')
        self.stocks.refresh_news()
        news = self.stocks.get_ticker_news('TSLA')
        self.assertIsNotNone(news)

    def test_refresh_data_for_ticker(self):
        # Test the specific ticker refresh method
        ticker = 'AMZN'
        self.stocks.add_ticker(ticker)
        self.stocks.refresh_data_for_ticker(ticker)
        
        data = self.stocks.get_ticker_data(ticker)
        self.assertIsNotNone(data)
        self.assertTrue(len(data) > 0)

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        import os
        if os.path.exists('test_stocks.db'):
            os.remove('test_stocks.db')

if __name__ == '__main__':
    unittest.main()
