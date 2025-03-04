import sys
import os

# Get the absolute path of the src directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
from stocks.stocks import Stocks
from stocks.database import Database
class TestStocks(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = Database('test_stocks.db')
        cls.stocks = Stocks(cls.db.connection)  # Pass the connection attributebute

    def test_add_ticker(self):
        self.stocks.add_ticker('AAPL')
        tickers = self.stocks.get_all_tickers()
        self.assertIn('AAPL', tickers)

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
