# Stock Data Library

## Overview
The Stock Data Library is a Python library designed to manage stock data using a SQLite database. It allows users to add and remove stock tickers, refresh stock data from Yahoo Finance, and fetch related news articles. The library is structured to facilitate easy integration and usage in various applications.

## Features
- Manage stock tickers in a SQLite database.
- Fetch and update stock data from Yahoo Finance.
- Retrieve news articles related to stock tickers.
- Handle duplicates in news data efficiently.

## Installation
To install the Stock Data Library, clone the repository and install the required packages:

```bash
git clone <repository-url>
cd stock-data-library
pip install -r requirements.txt
```

## Usage
Here is a basic example of how to use the Stocks class:

```python
from stocks import Stocks

# Initialize the Stocks class
stocks = Stocks()

# Add a new ticker
stocks.add_ticker('AAPL')

# Refresh stock data
stocks.refresh_data()

# Remove a ticker
stocks.remove_ticker('AAPL')
```

For more detailed examples, please refer to the `examples` directory.

## Testing
To run the tests for the library, navigate to the project directory and execute:

```bash
pytest tests/
```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure that your code adheres to the project's coding standards and includes appropriate tests.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.