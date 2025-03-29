from setuptools import setup, find_packages

setup(
    name='stock-data-library',
    version='0.1.0',
    author='Boxplot Inc.',
    author_email='your.email@example.com',
    description='A library for managing stock data using SQLite and Yahoo Finance.',
    packages=['stocks'],  # Explicitly define the package
    package_dir={'stocks': 'src/stocks'},  # Map the package to the correct directory
    install_requires=[
        'yfinance',  # Yahoo Finance library
        'pandas',    # For data manipulation
        'textblob',  # For sentiment analysis
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)