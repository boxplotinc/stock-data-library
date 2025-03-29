from src.stocks.stocks import Stocks
from src.stocks.database import Database

stocks_database = Database('stocks.db')
stocks = Stocks(stocks_database.connection)

# tickers = [
#     # Stock Market Indexes
#     "^GSPC",  # S&P 500
#     "^DJI",   # Dow Jones Industrial Average (DJIA)
#     "^IXIC",  # NASDAQ Composite
#     "^FTSE",  # FTSE 100
#     "^GDAXI", # DAX (Germany)
#     "^FCHI",  # CAC 40 (France)
#     "^N225",  # Nikkei 225 (Japan)
#     "000001.SS",  # Shanghai Composite Index
#     "^HSI",   # Hang Seng Index
#     "^BSESN", # BSE Sensex (India)
#     "^GSPTSE",  # S&P/TSX Composite Index (Canada)
#     "^AXJO",  # ASX 200 (Australia)
#     "^KS11",  # KOSPI (South Korea)
#     "^TWII",  # Taiwan Weighted Index
#     "FTSEMIB.MI", # FTSE MIB (Italy)
#     "^IBEX",  # IBEX 35 (Spain)
#     "^SSMI",  # SMI (Swiss Market Index)
#     "^BVSP",  # Bovespa Index (Brazil)
#     "^STOXX50E",  # EURO STOXX 50 (Eurozone)
#     "^AORD",  # All Ordinaries (Australia)
#     "^MXX",  # IPC (Mexican Stock Exchange)
#     "^RUT",  # Russell 2000 (U.S. Small-Cap Index)
#     "^NZ50",  # S&P/NZX 50 Index (New Zealand)
#     "^JKSE",  # Jakarta Composite Index (Indonesia)
#     "^SET.BK",  # SET Index (Thailand)
#     "PSEI.PS",  # PSEi (Philippines)
#     "^TA125.TA",  # TA-125 Index (Israel)
#     "^OSEAX",  # Oslo All-Share Index (Norway)
    
#     # Emerging Markets Indexes
#     "^MSCI",  # MSCI World Index
#     "EEM",  # iShares MSCI Emerging Markets ETF
#     "^MERV",  # MERVAL (Argentina)
#     "^XU100",  # BIST 100 (Turkey)
#     "^JTOPI",  # FTSE/JSE Top 40 (South Africa)

#     # Bond Yields
#     '^IRX',  # 1-Month Treasury Yield
#     '^IRX',  # 3-Month Treasury Yield (same as 1-Year Yield)
#     '^FVX',  # 6-Month Treasury Yield
#     '^IRX',  # 1-Year Treasury Yield
#     '^TNX',  # 2-Year Treasury Yield
#     '^FVX',  # 5-Year Treasury Yield
#     '^TYX',  # 7-Year Treasury Yield
#     "^TNX",  # U.S. 10-Year Treasury Yield
#     "^TYX",  # U.S. 30-Year Treasury Yield
#     "^LTT",  # Long-Term Treasury Bond Yield
#     "^T10Y2Y",  # U.S. 10-Year minus 2-Year Treasury Spread (Recession Indicator)

#     # Commodities
#     "CL=F",   # WTI Crude Oil Price
#     "BZ=F",   # Brent Crude Oil Price
#     "GC=F",   # Gold Spot Price
#     "HG=F",   # Copper Spot Price
#     "NG=F",   # Natural Gas Price (Henry Hub)
#     "SI=F",   # Silver Spot Price
#     "PL=F",   # Platinum Spot Price
#     "ZC=F",   # Corn Futures Price
#     "ZS=F",   # Soybean Futures Price
#     "PA=F",   # Palladium Spot Price
#     "KC=F",   # Coffee Futures
#     "SB=F",   # Sugar Futures
#     "CC=F",   # Cocoa Futures
#     "LE=F",   # Live Cattle Futures

#     # Volatility Indexes
#     "^VIX",   # CBOE Volatility Index
#     "^VXN",   # NASDAQ Volatility Index
#     "^VVIX",  # Volatility of VIX (Meta-Volatility)
#     "^MOVE",  # Bond Market Volatility Index

#     # Currency & FX Indexes
#     "DX-Y.NYB",  # U.S. Dollar Index (DXY)
#     "EURUSD=X",  # EUR/USD Exchange Rate
#     "USDJPY=X",  # USD/JPY Exchange Rate
#     "GBPUSD=X",  # GBP/USD Exchange Rate
#     "USDCHF=X",  # USD/CHF Exchange Rate
#     "USDCNY=X",  # USD/CNY Exchange Rate
#     "USDBRL=X",  # USD/BRL Exchange Rate
#     "JPYCNY=X",   # JPY/CNY Exchange Rate (Yen to Yuan)
#     "^CXY"       # China Currency Index
# ]


# for ticker in tickers:
#     stocks.add_ticker(ticker, '2024-01-01', '2025-03-11')

# symbols = ["^PSEI", "^OSEAX.OL", "^MSCI", "^XU100", "^SA40", "^LTT", "^T10Y2Y", "^JPYCNY", "^CXY"]

# for ticker in symbols:
#     stocks.remove_ticker(ticker)
# stocks.remove_ticker('^JTOPI')
# stocks.refresh_data(start_date='1996-01-01', end_date='1999-12-31')
stocks.add_ticker('META', '2015-01-01', '2025-03-12')
# stocks.refresh_data_for_ticker('AAPL', '2015-01-01', '2019-12-31')
# stocks.refresh_news()
# stocks_database.get_ticker_data('INTC')