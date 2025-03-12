from setuptools import setup, find_packages

setup(
    name='stock-data-library',
    version='0.1.0',
    author='Boxplot Inc.',
    author_email='your.email@example.com',
    description='A library for managing stock data using SQLite and Yahoo Finance.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'yfinance',  # Yahoo Finance library
        'pandas',    # For data manipulation
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    include_package_data=False,
)