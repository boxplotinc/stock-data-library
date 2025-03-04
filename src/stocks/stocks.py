class Stocks:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.create_tables()

    def create_tables(self):
        cursor = self.db_connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tickers (
                ticker TEXT PRIMARY KEY
            )
        ''')
        cursor.execute('''
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
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ticker_news (
                ticker TEXT,
                date DATE,
                news_id TEXT,
                news_summary TEXT,
                sentiment TEXT,
                PRIMARY KEY (ticker, date, news_id)
            )
        ''')
        self.db_connection.commit()

    def add_ticker(self, ticker):
        """
        Adds a ticker to the database if it doesn't already exist.
        Then refreshes data for that ticker.
        """
        cursor = self.db_connection.cursor()
        
        # First check if ticker already exists
        cursor.execute('SELECT 1 FROM tickers WHERE ticker = ?', (ticker,))
        exists = cursor.fetchone() is not None
        
        if not exists:
            try:
                cursor.execute('INSERT INTO tickers (ticker) VALUES (?)', (ticker,))
                self.db_connection.commit()
                print(f"Added ticker: {ticker}")
                # Only refresh data for newly added tickers
                self.refresh_data_for_ticker(ticker)
            except Exception as e:
                self.db_connection.rollback()
                print(f"Error adding ticker {ticker}: {e}")
        else:
            print(f"Ticker {ticker} already exists in database")

    def remove_ticker(self, ticker):
        cursor = self.db_connection.cursor()
        cursor.execute('DELETE FROM tickers WHERE ticker = ?', (ticker,))
        cursor.execute('DELETE FROM ticker_data WHERE ticker = ?', (ticker,))
        self.db_connection.commit()

    def refresh_data(self):
        """
        Refreshes stock data for all tickers in the database.
        For existing tickers, fetches data since the most recent date in database.
        For new tickers, fetches up to 10 years of historical data.
        """
        import yfinance as yf
        import pandas as pd
        from datetime import datetime, timedelta

        cursor = self.db_connection.cursor()
        # Get all tickers from the database
        cursor.execute('SELECT ticker FROM tickers')
        tickers = [row[0] for row in cursor.fetchall()]
        
        if not tickers:
            return  # No tickers to refresh
        
        today = datetime.now().date()
        
        for ticker in tickers:
            # Find the most recent data point for this ticker
            cursor.execute(
                'SELECT MAX(date) FROM ticker_data WHERE ticker = ?', 
                (ticker,)
            )
            last_date_row = cursor.fetchone()
            last_date = last_date_row[0]
            
            start_date = None
            if last_date is None:
                # No existing data for this ticker, get 10 years of history
                start_date = (today - timedelta(days=10)).strftime('%Y-%m-%d')
            else:
                # Get data since the last recorded date (add 1 day to avoid duplication)
                from datetime import datetime
                last_date = datetime.strptime(last_date, '%Y-%m-%d').date()
                start_date = (last_date + timedelta(days=1)).strftime('%Y-%m-%d')
                
                # If last date is today or in future, skip this ticker
                if last_date >= today:
                    continue
                    
            # Fetch data from Yahoo Finance
            try:
                ticker_obj = yf.Ticker(ticker)
                df = ticker_obj.history(start=start_date, end=today.strftime('%Y-%m-%d'))
                
                if df.empty:
                    continue
                    
                # Prepare and insert data
                for index, row in df.iterrows():
                    date = index.strftime('%Y-%m-%d')
                    cursor.execute('''
                        INSERT OR REPLACE INTO ticker_data 
                        (ticker, date, open, high, low, close, volume, dividends, stocksplits) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        ticker,
                        date,
                        row['Open'],
                        row['High'],
                        row['Low'],
                        row['Close'],
                        row['Volume'],
                        row.get('Dividends', 0),
                        row.get('Stock Splits', 0)
                    ))
                
                self.db_connection.commit()
                
            except Exception as e:
                print(f"Error fetching data for {ticker}: {e}")
                # Continue with the next ticker rather than failing completely
                continue

    def refresh_news(self):
        """
        Fetches recent news for all stock tickers in the database.
        Ignores indices (tickers starting with ^).
        Avoids duplicate news entries based on news_id.
        """
        import yfinance as yf
        from datetime import datetime
        import hashlib
        
        cursor = self.db_connection.cursor()
        # Get all stock tickers (exclude indices starting with ^)
        cursor.execute("SELECT ticker FROM tickers WHERE ticker NOT LIKE '^%'")
        tickers = [row[0] for row in cursor.fetchall()]
        
        if not tickers:
            return  # No tickers to refresh
        
        for ticker in tickers:
            try:
                ticker_obj = yf.Ticker(ticker)
                news_items = ticker_obj.get_news(count=10)
                
                if not news_items:
                    continue
                    
                for item in news_items:
                    # Generate a unique ID for the news item if it doesn't have one
                    if 'id' in item:
                        news_id = item['id']
                    else:
                        # Create a hash from the title and publish date as a unique ID
                        news_id = hashlib.md5(f"{item.get('title', '')}{item.get('publishedAt', '')}".encode()).hexdigest()
                    
                    # Convert timestamp to date
                    if 'pubDate' in item['content']:
                        news_date = datetime.fromisoformat(item['content']['pubDate'].replace("Z", "+00:00"))
                    else:
                        news_date = datetime.now().strftime('%Y-%m-%d')

                    # Get the news summary
                    summary = item['content'].get('summary')
                    if not summary and 'title' in item['content']:
                        summary = item['content'].get('title')
                    
                    # Simple sentiment analysis placeholder
                    # In a real implementation, you would use a sentiment analysis library
                    sentiment = 'neutral'
                    
                    # Insert or replace the news item
                    cursor.execute('''
                        INSERT OR REPLACE INTO ticker_news 
                        (ticker, date, news_id, news_summary, sentiment) 
                        VALUES (?, ?, ?, ?, ?)
                    ''', (ticker, news_date, news_id, summary, sentiment))
                
                self.db_connection.commit()
                
            except Exception as e:
                print(f"Error fetching news for {ticker}: {e}")
                continue

    def get_all_tickers(self):
        """Return a list of all tickers in the database"""
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT ticker FROM tickers')
        return [row[0] for row in cursor.fetchall()]

    def get_ticker_data(self, ticker):
        """Return all data for a specific ticker"""
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT * FROM ticker_data WHERE ticker = ? ORDER BY date DESC', (ticker,))
        return cursor.fetchall()

    def get_ticker_news(self, ticker):
        """Return all news for a specific ticker"""
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT * FROM ticker_news WHERE ticker = ? ORDER BY date DESC', (ticker,))
        return cursor.fetchall()

    def refresh_data_for_ticker(self, ticker):
        """
        Refreshes stock data for a specific ticker.
        """
        import yfinance as yf
        from datetime import datetime, timedelta
        
        cursor = self.db_connection.cursor()
        today = datetime.now().date()
        
        # Find the most recent data point for this ticker
        cursor.execute(
            'SELECT MAX(date) FROM ticker_data WHERE ticker = ?', 
            (ticker,)
        )
        last_date_row = cursor.fetchone()
        last_date = last_date_row[0]
        
        start_date = None
        if last_date is None:
            # No existing data for this ticker, get 10 years of history
            start_date = (today - timedelta(days=10)).strftime('%Y-%m-%d')
        else:
            # Get data since the last recorded date (add 1 day to avoid duplication)
            from datetime import datetime
            last_date = datetime.strptime(last_date, '%Y-%m-%d').date()
            start_date = (last_date + timedelta(days=1)).strftime('%Y-%m-%d')
            
            # If last date is today or in future, skip this ticker
            if last_date >= today:
                return
                    
        # Fetch data from Yahoo Finance
        try:
            ticker_obj = yf.Ticker(ticker)
            df = ticker_obj.history(start=start_date, end=today.strftime('%Y-%m-%d'))
            
            if df.empty:
                return
                
            # Prepare and insert data
            for index, row in df.iterrows():
                date = index.strftime('%Y-%m-%d')
                cursor.execute('''
                    INSERT OR REPLACE INTO ticker_data 
                    (ticker, date, open, high, low, close, volume, dividends, stocksplits) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    ticker,
                    date,
                    row['Open'],
                    row['High'],
                    row['Low'],
                    row['Close'],
                    row['Volume'],
                    row.get('Dividends', 0),
                    row.get('Stock Splits', 0)
                ))
            
            self.db_connection.commit()
            
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")