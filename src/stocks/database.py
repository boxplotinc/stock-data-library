import sqlite3

class Database:
    def __init__(self, db_name='stocks.db'):
        self.connection = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS tickers (
                    ticker TEXT PRIMARY KEY
                )
            ''')
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS ticker_data (
                    ticker TEXT,
                    date DATE,
                    open NUMERIC,
                    high NUMERIC,
                    low NUMERIC,
                    close NUMERIC,
                    volume NUMERIC,
                    dividends NUMERIC,
                    stocksplits NUMERIC,
                    PRIMARY KEY (ticker, date)
                )
            ''')
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS ticker_news (
                    ticker TEXT,
                    date DATE,
                    news_id TEXT,
                    news_summary TEXT,
                    sentiment TEXT,
                    PRIMARY KEY (ticker, date, news_id)
                )
            ''')

    def add_ticker(self, ticker):
        with self.connection:
            self.connection.execute('INSERT INTO tickers (ticker) VALUES (?)', (ticker,))

    def remove_ticker(self, ticker):
        with self.connection:
            self.connection.execute('DELETE FROM tickers WHERE ticker = ?', (ticker,))
            self.connection.execute('DELETE FROM ticker_data WHERE ticker = ?', (ticker,))

    def fetch_tickers(self):
        """Returns a list of all tickers in the database"""
        cursor = self.connection.cursor()
        cursor.execute('SELECT ticker FROM tickers')
        return [row[0] for row in cursor.fetchall()]

    def insert_ticker_data(self, ticker, date, open_price, high, low, close, volume, dividends, stocksplits):
        """Inserts stock data for a ticker on a specific date"""
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO ticker_data 
            (ticker, date, open, high, low, close, volume, dividends, stocksplits) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (ticker, date, open_price, high, low, close, volume, dividends, stocksplits))
        self.connection.commit()

    def fetch_ticker_data(self, ticker):
        """Returns all data for a specific ticker"""
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM ticker_data WHERE ticker = ? ORDER BY date DESC', (ticker,))
        return cursor.fetchall()

    def insert_ticker_news(self, ticker, date, news_id, news_summary, sentiment):
        """Inserts news for a ticker on a specific date"""
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO ticker_news 
            (ticker, date, news_id, news_summary, sentiment) 
            VALUES (?, ?, ?, ?, ?)
        ''', (ticker, date, news_id, news_summary, sentiment))
        self.connection.commit()

    def fetch_ticker_news(self, ticker):
        """Returns all news for a specific ticker"""
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM ticker_news WHERE ticker = ? ORDER BY date DESC', (ticker,))
        return cursor.fetchall()

    def close(self):
        self.connection.close()