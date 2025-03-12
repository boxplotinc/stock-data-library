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

    def test_refresh_news(self):
        self.stocks.add_ticker('TSLA')
        self.stocks.refresh_news()
        news = self.stocks.get_ticker_news('TSLA')
        self.assertIsNotNone(news)

    # Update tearDownClass to remove the test database
    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        import os
        if os.path.exists('test_stocks.db'):
            os.remove('test_stocks.db')

if __name__ == '__main__':
    unittest.main()
