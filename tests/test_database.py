import sys
import os

# Get the absolute path of the src directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
import sqlite3
import sys
from stocks.database import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database('test_stocks.db')
        self.db.create_tables()

    def tearDown(self):
        self.db.close()
        import os
        os.remove('test_stocks.db')

    def test_create_tables(self):
        connection = sqlite3.connect('test_stocks.db')
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        expected_tables = ['tickers', 'ticker_data', 'ticker_news']
        self.assertTrue(all(table in table_names for table in expected_tables))
        connection.close()

    def test_add_ticker(self):
        self.db.add_ticker('AAPL')
        tickers = self.db.fetch_tickers()
        self.assertIn('AAPL', tickers)

    def test_remove_ticker(self):
        self.db.add_ticker('AAPL')
        self.db.remove_ticker('AAPL')
        tickers = self.db.fetch_tickers()
        self.assertNotIn('AAPL', tickers)

    def test_ticker_data_insertion(self):
        self.db.add_ticker('AAPL')
        self.db.insert_ticker_data('AAPL', '2023-01-01', 150, 155, 148, 153, 1000000, 0, 0)
        data = self.db.fetch_ticker_data('AAPL')
        self.assertEqual(len(data), 1)

    def test_ticker_news_insertion(self):
        self.db.add_ticker('AAPL')
        self.db.insert_ticker_news('AAPL', '2023-01-01', 'news_id_1', 'Apple releases new product', 'positive')
        news = self.db.fetch_ticker_news('AAPL')
        self.assertEqual(len(news), 1)

if __name__ == '__main__':
    unittest.main()