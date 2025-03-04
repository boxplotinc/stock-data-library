def format_date(date):
    return date.strftime('%Y-%m-%d')

def parse_date(date_string):
    from datetime import datetime
    return datetime.strptime(date_string, '%Y-%m-%d').date()

def is_valid_ticker(ticker):
    return isinstance(ticker, str) and len(ticker) > 0 and not ticker.startswith('^')

def sanitize_input(input_value):
    if isinstance(input_value, str):
        return input_value.strip()
    return input_value