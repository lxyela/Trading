# Description: This script downloads the stock price data from yahoo finance

from datetime import datetime
import yfinance as yf
import os
from utils.methods import *

def download_data(start_date='', end_date='', symbol='', interval='1m', dest_folder='./'):
    """
    This function downloads the stock price data from yahoo finance
    :param start_date: start date of the data to be downloaded
    :param end_date: end date of the data to be downloaded
    :param symbol: stock symbol
    :param interval: interval of the data to be downloaded, default is 1 minute interval
    :param dest_folder: destination folder to save the data if not specified the data will be saved in the current folder
    :return: returns a csv file with the stock price data for the specified date range and stock symbol in the destination folder

    sample usage: download_data(start_date='2020-01-01', end_date='2020-01-02', symbol='AAPL', interval='1m', dest_folder='./data')
    """
    # check if the date arguments are in the correct format
    start_date = check_date_format(start_date, date_format='%Y-%m-%d')
    end_date = check_date_format(start_date, date_format='%Y-%m-%d')
    run_date = datetime.now()
    
    # check if the symbol is a string
    if not isinstance(symbol, str):
        raise ValueError('Symbol should be a string')
    
    # check if the destination folder is a string
    if not isinstance(dest_folder, str):
        raise ValueError('Destination folder should be a string')
    
    # check if the destintion folder is a valid path
    dest_folder = check_file_folder(dest_folder)

    dest_folder = os.path.join(dest_folder, 'data', 'yahoo_data')
    # check if dest_folder exists, if not create it
    print(dest_folder)
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # if the interval is not 1m or 5m or 15m raise an error
    if interval not in ['1m', '2m', '5m', '15m', '30m', '60m', '1h', '1d', '5d', '1wk']:
        raise ValueError('Interval should be 1m, 5m, 15m, 30m, 60m, 1h, 1d, 5d, 1wk')

    # if the interval is 1m, the date range should be less than or equal to 7 days and the data should be with in 30 days from the current date
    if interval == '1m':
        # raise an error if the date range is greater than 7 days
        if (end_date - start_date).days > 7:
            raise ValueError('Date range should be less than or equal to 7 days')
        
        # raise an error if the date range is greater than 30 days
        if (run_date - start_date).days > 30:
                raise ValueError('Start date should be less than or equal to 30 days from the current date')
    
    elif interval == '5m' or interval == '15m':
        # raise an error if the date range is greater than 60 days
        if (run_date - start_date).days >= 60:
                raise ValueError('Start date should be less than or equal to 60 days from the current date')
        
    elif interval == '1h':
        # raise an error if the date range is greater than 730 days
        if (run_date - start_date).days >= 730:
                raise ValueError('Start date should be less than or equal to 730 days from the current date')
    
    #download the stock price 1 minute interval data using yfinance library
    data = yf.download(symbol, start=start_date, end=end_date, interval=interval)

    try:
         # Convert the time zone to US/Eastern
        data.index = data.index.tz_convert('US/Eastern')
    except:
        # use tz_localize to localize the time zone to UTC
        data.index = data.index.tz_localize('US/Eastern')
        
    # save the data to a csv file with the name of the stock symbol and the date range in the file name to a specific folder
    data.to_csv(f'{dest_folder}/{symbol}_{interval}_{start_date.strftime("%Y-%m-%d")}_{end_date.strftime("%Y-%m-%d")}.csv')

    return data