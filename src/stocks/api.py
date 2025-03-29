import yfinance as yf

def get_stock_data(ticker, start_date, end_date):
    """Get stock data from Yahoo Finance API."""
    ticker_obj = yf.Ticker(ticker)
    return ticker_obj.history(start=start_date, end=end_date)

def get_stock_news(ticker):
    """Get news for a ticker from Yahoo Finance API."""
    ticker_obj = yf.Ticker(ticker)
    return ticker_obj.get_news()