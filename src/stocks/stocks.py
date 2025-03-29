import logging
from datetime import datetime, timedelta
from typing import List, Tuple, Union, Optional, Dict, Any

# Import utils functions
from .utils import format_date, parse_date, sanitize_input

logger = logging.getLogger(__name__)

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

    def add_ticker(self, ticker, start_date=None, end_date=None):
        """
        Adds a ticker to the database if it doesn't already exist.
        Then refreshes data for that ticker for the specified date range.
        
        Parameters:
        ticker (str): The ticker symbol to add
        start_date (str or datetime, optional): Start date in format 'YYYY-MM-DD'. If None, 
                                               uses most recent data in DB or 10 years ago
        end_date (str or datetime, optional): End date in format 'YYYY-MM-DD'. If None, uses today's date
        """
        with self.db_connection:  # This automatically handles commit/rollback
            cursor = self.db_connection.cursor()
            
            # First check if ticker already exists
            cursor.execute('SELECT 1 FROM tickers WHERE ticker = ?', (ticker,))
            exists = cursor.fetchone() is not None
            
            if not exists:
                try:
                    cursor.execute('INSERT INTO tickers (ticker) VALUES (?)', (ticker,))
                    logger.info(f"Added ticker: {ticker}")
                    # Only refresh data for newly added tickers, passing along date parameters
                    self.refresh_data_for_ticker(ticker, start_date, end_date)
                except Exception as e:
                    logger.error(f"Error adding ticker {ticker}: {e}")
            else:
                print(f"Ticker {ticker} already exists in database")

    def remove_ticker(self, ticker):
        cursor = self.db_connection.cursor()
        cursor.execute('DELETE FROM tickers WHERE ticker = ?', (ticker,))
        cursor.execute('DELETE FROM ticker_data WHERE ticker = ?', (ticker,))
        self.db_connection.commit()

    def refresh_data(self, start_date=None, end_date=None):
        """
        Refreshes stock data for all tickers in the database.
        
        Parameters:
        start_date (str or datetime, optional): Start date in format 'YYYY-MM-DD'. If None, 
                                               uses most recent data in DB or 10 years ago
        end_date (str or datetime, optional): End date in format 'YYYY-MM-DD'. If None, uses today's date
        """
        cursor = self.db_connection.cursor()
        # Get all tickers from the database
        cursor.execute('SELECT ticker FROM tickers')
        tickers = [row[0] for row in cursor.fetchall()]
        
        if not tickers:
            print("No tickers found in database")
            return  # No tickers to refresh
        
        print(f"Refreshing data for {len(tickers)} tickers...")
        for ticker in tickers:
            self.refresh_data_for_ticker(ticker, start_date, end_date)

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
            logger.info("No tickers found for news refresh")
            return  # No tickers to refresh
        
        news_count = 0
        for ticker in tickers:
            try:
                ticker_obj = yf.Ticker(ticker)
                news_items = ticker_obj.get_news(count=1000)
                
                if not news_items:
                    logger.debug(f"No news found for {ticker}")
                    continue
                
                ticker_news_count = 0    
                for item in news_items:
                    # Generate a unique ID for the news item if it doesn't have one
                    if 'id' in item:
                        news_id = item['id']
                    else:
                        # Create a hash from the title and publish date as a unique ID
                        news_id = hashlib.md5(f"{item.get('title', '')}{item.get('publishedAt', '')}".encode()).hexdigest()
                    
                    # Convert timestamp to date
                    if 'pubDate' in item['content']:
                        try:
                            news_date = datetime.fromisoformat(item['content']['pubDate'].replace("Z", "+00:00"))
                            news_date = news_date.strftime('%Y-%m-%d')
                        except (ValueError, TypeError):
                            news_date = datetime.now().strftime('%Y-%m-%d')
                    else:
                        news_date = datetime.now().strftime('%Y-%m-%d')

                    # Get the news summary
                    summary = item['content'].get('summary')
                    if not summary and 'title' in item['content']:
                        summary = item['content'].get('title')
                    
                    # Use the analyze_sentiment function
                    sentiment = analyze_sentiment(summary) if summary else 'neutral'
                    
                    # Insert or replace the news item
                    cursor.execute('''
                        INSERT OR REPLACE INTO ticker_news 
                        (ticker, date, news_id, news_summary, sentiment) 
                        VALUES (?, ?, ?, ?, ?)
                    ''', (ticker, news_date, news_id, summary, sentiment))
                    ticker_news_count += 1
                
                self.db_connection.commit()
                news_count += ticker_news_count
                logger.info(f"Added/updated {ticker_news_count} news items for {ticker}")
                
            except Exception as e:
                logger.error(f"Error fetching news for {ticker}: {str(e)}")
                continue
        
        logger.info(f"Total news items processed: {news_count}")

    def get_all_tickers(self) -> List[str]:
        """
        Return a list of all tickers in the database
        
        Returns:
            List[str]: List of ticker symbols
        """
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT ticker FROM tickers')
        return [row[0] for row in cursor.fetchall()]

    def get_ticker_data(self, ticker: str, start_date: Optional[Union[str, datetime]] = None, 
                        end_date: Optional[Union[str, datetime]] = None) -> List[Tuple]:
        """
        Return data for a specific ticker, optionally filtered by date range.
        
        Parameters:
            ticker (str): The ticker symbol to get data for
            start_date (str or datetime, optional): Start date in format 'YYYY-MM-DD'
            end_date (str or datetime, optional): End date in format 'YYYY-MM-DD'
        
        Returns:
            list: List of tuples containing ticker data ordered by date (descending)
        """
        cursor = self.db_connection.cursor()
        
        # Sanitize inputs
        ticker = sanitize_input(ticker)
        
        # Convert datetime objects to strings if necessary
        if start_date and isinstance(start_date, datetime):
            start_date = format_date(start_date)
        
        if end_date and isinstance(end_date, datetime):
            end_date = format_date(end_date)
        
        # Build the query based on provided parameters
        query = 'SELECT * FROM ticker_data WHERE ticker = ?'
        params = [ticker]
        
        if start_date and end_date:
            query += ' AND date BETWEEN ? AND ?'
            params.extend([start_date, end_date])
        elif start_date:
            query += ' AND date >= ?'
            params.append(start_date)
        elif end_date:
            query += ' AND date <= ?'
            params.append(end_date)
        
        query += ' ORDER BY date DESC'
        
        # Execute the query with appropriate parameters
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()
            
            if not result:
                logger.info(f"No data found for ticker {ticker} in the specified date range")
            else:
                logger.info(f"Retrieved {len(result)} data points for ticker {ticker}")
            
            return result
        except Exception as e:
            logger.error(f"Error retrieving data for {ticker}: {str(e)}")
            return []

    def get_ticker_news(self, ticker):
        """Return all news for a specific ticker"""
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT * FROM ticker_news WHERE ticker = ? ORDER BY date DESC', (ticker,))
        return cursor.fetchall()

    def refresh_data_for_ticker(self, ticker, start_date=None, end_date=None):
        """
        Refreshes stock data for a specific ticker.
        
        Parameters:
        ticker (str): The ticker symbol to refresh data for
        start_date (str or datetime, optional): Start date in format 'YYYY-MM-DD'. If None, 
                                               uses most recent data in DB or 10 years ago
        end_date (str or datetime, optional): End date in format 'YYYY-MM-DD'. If None, uses today's date
        """
        import yfinance as yf
        from datetime import datetime, timedelta
        
        cursor = self.db_connection.cursor()
        today = datetime.now().date()
        
        # Set end_date if not provided
        if end_date is None:
            end_date = today.strftime('%Y-%m-%d')
        elif isinstance(end_date, datetime):
            end_date = end_date.strftime('%Y-%m-%d')
            
        # If start_date is provided, use it directly
        if start_date is not None:
            if isinstance(start_date, datetime):
                start_date = start_date.strftime('%Y-%m-%d')
        else:
            # Find the most recent data point for this ticker
            cursor.execute(
                'SELECT MAX(date) FROM ticker_data WHERE ticker = ?', 
                (ticker,)
            )
            last_date_row = cursor.fetchone()
            last_date = last_date_row[0]
            
            if last_date is None:
                # No existing data for this ticker, get 10 years of history
                start_date = (today - timedelta(days=365*10)).strftime('%Y-%m-%d')
            else:
                # Get data since the last recorded date (add 1 day to avoid duplication)
                last_date = datetime.strptime(last_date, '%Y-%m-%d').date()
                start_date = (last_date + timedelta(days=1)).strftime('%Y-%m-%d')
                
                # If last date is at or after end_date, nothing to do
                if last_date >= datetime.strptime(end_date, '%Y-%m-%d').date():
                    return
                    
        # Fetch data from Yahoo Finance
        try:
            ticker_obj = yf.Ticker(ticker)
            df = ticker_obj.history(start=start_date, end=end_date)
            
            if df.empty:
                print(f"No data found for {ticker} between {start_date} and {end_date}")
                return
                
            # Prepare and insert data
            data_to_insert = []
            for index, row in df.iterrows():
                date = index.strftime('%Y-%m-%d')
                data_to_insert.append((
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
            
            # Instead of committing after each insert
            cursor.executemany('''
                INSERT OR REPLACE INTO ticker_data 
                (ticker, date, open, high, low, close, volume, dividends, stocksplits) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', data_to_insert)
            self.db_connection.commit()
            print(f"Refreshed {len(df)} data points for {ticker} from {start_date} to {end_date}")
            
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")

def analyze_sentiment(text):
    """
    Simple sentiment analysis using TextBlob.
    
    Parameters:
        text (str): The text to analyze
        
    Returns:
        str: Sentiment classification ('positive', 'negative', or 'neutral')
    """
    try:
        from textblob import TextBlob
        analysis = TextBlob(text)
        # Determine if positive, negative, or neutral
        polarity = analysis.sentiment.polarity
        if polarity > 0.1:
            return 'positive'
        elif polarity < -0.1:
            return 'negative'
        else:
            return 'neutral'
    except Exception:
        # In case TextBlob isn't installed or other errors
        return 'neutral'