from datetime import datetime
from typing import Union, Optional, Any

def format_date(date: Union[datetime, Any]) -> str:
    """
    Convert a datetime object to string format 'YYYY-MM-DD'
    
    Parameters:
        date (datetime): Date to format
        
    Returns:
        str: Formatted date string
    """
    if isinstance(date, datetime):
        return date.strftime('%Y-%m-%d')
    elif hasattr(date, 'strftime'):
        return date.strftime('%Y-%m-%d')
    return str(date)

def parse_date(date_string: Union[str, Any]) -> datetime.date:
    """
    Parse a date string into a datetime.date object
    
    Parameters:
        date_string (str): Date string in format 'YYYY-MM-DD'
        
    Returns:
        datetime.date: Parsed date object
        
    Raises:
        ValueError: If the date_string is not in the correct format
    """
    if isinstance(date_string, datetime):
        return date_string.date()
    
    try:
        return datetime.strptime(str(date_string), '%Y-%m-%d').date()
    except ValueError:
        raise ValueError(f"Date '{date_string}' is not in format 'YYYY-MM-DD'")

def is_valid_ticker(ticker: str) -> bool:
    """
    Verify if a ticker symbol is valid
    
    Parameters:
        ticker (str): Ticker symbol to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    return isinstance(ticker, str) and len(ticker) > 0

def sanitize_input(input_value: Any) -> Any:
    """
    Sanitize user input
    
    Parameters:
        input_value (Any): Value to sanitize
        
    Returns:
        Any: Sanitized value
    """
    if isinstance(input_value, str):
        return input_value.strip()
    return input_value

def get_date_range(start_date: Optional[str] = None, end_date: Optional[str] = None, 
                  default_days: int = 365*10) -> tuple:
    """
    Get a validated date range with sensible defaults
    
    Parameters:
        start_date (str, optional): Start date string
        end_date (str, optional): End date string
        default_days (int): Default number of days for lookback if start_date not specified
        
    Returns:
        tuple: (start_date, end_date) as string dates in format 'YYYY-MM-DD'
    """
    today = datetime.now().date()
    
    # Set end_date (today if not specified)
    if not end_date:
        end_date = format_date(today)
    elif not isinstance(end_date, str):
        end_date = format_date(end_date)
    
    # Set start_date (10 years ago if not specified)
    if not start_date:
        start_date = format_date(today - timedelta(days=default_days))
    elif not isinstance(start_date, str):
        start_date = format_date(start_date)
    
    return (start_date, end_date)