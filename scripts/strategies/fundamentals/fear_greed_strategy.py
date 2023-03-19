import requests
import pandas as pd
from datetime import datetime
import sys
sys.path.append('./scripts')
from utils.methods import *

cnn_backend_url = 'https://production.dataviz.cnn.io/'
cnn_fear_greed_index_url = cnn_backend_url + 'index/fearandgreed/graphdata/{}'

# Get today's date
today = datetime.today().strftime('%Y-%m-%d')

# Get the latest fear and greed index from CNN
def get_fear_greed_index(date=today, file_name='fear_greed_index.csv', dest_folder='./'):
    """
    Get the latest fear and greed index from CNN
    """
    # date could be either list or string
    if isinstance(date, str):
        date = [date]

    # check if the destintion folder is a valid path
    dest_folder = check_file_folder(dest_folder)
    
    # Get the data
    fear_greed_list = []
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
    for d in date:
        response = requests.get(cnn_fear_greed_index_url.format(d), headers=headers)
        if response.status_code != 200:
            print('Error: {}'.format(response.status_code))
            raise Exception('Error: {}\nThis might me be due to the bot blockers at the application server.'.format(response.status_code))
        fear_greed_dict = {}
        data = response.json()
        # Parse the data
        fear_greed_dict['fear_and_greed_score'] = round(data['market_momentum_sp500']['score'], 2)
        fear_greed_dict['timestamp'] = data['fear_and_greed']['timestamp'][:-6]
        fear_greed_dict['fear_and_greed_rating'] = data['fear_and_greed']['rating'] 

        fear_greed_dict['market_momentum_sp500_score'] = round(data['market_momentum_sp500']['score'], 2)
        fear_greed_dict['market_momentum_sp500_rating'] = data['market_momentum_sp500']['rating']
        fear_greed_dict['market_momentum_sp500_data'] = round(data['market_momentum_sp500']['data'][0]['y'], 2)
        fear_greed_dict['market_momentum_sp500_data_rating'] = data['market_momentum_sp500']['data'][0]['rating']

        fear_greed_dict['market_momentum_sp125_score'] = round(data['market_momentum_sp125']['score'], 2)
        fear_greed_dict['market_momentum_sp125_rating'] = data['market_momentum_sp125']['rating']
        fear_greed_dict['market_momentum_sp125_data'] = round(data['market_momentum_sp125']['data'][0]['y'], 2)
        fear_greed_dict['market_momentum_sp125_data_rating'] = data['market_momentum_sp125']['data'][0]['rating']

        fear_greed_dict['stock_price_strength_score'] = round(data['stock_price_strength']['score'], 2)
        fear_greed_dict['stock_price_strength_rating'] = data['stock_price_strength']['rating']
        fear_greed_dict['stock_price_strength_data'] = round(data['stock_price_strength']['data'][0]['y'], 2)
        fear_greed_dict['stock_price_strength_data_rating'] = data['stock_price_strength']['data'][0]['rating']

        fear_greed_dict['stock_price_breadth_score'] = round(data['stock_price_breadth']['score'], 2)
        fear_greed_dict['stock_price_breadth_rating'] = data['stock_price_breadth']['rating']
        fear_greed_dict['stock_price_breadth_score_data'] = round(data['stock_price_breadth']['data'][0]['y'], 2)
        fear_greed_dict['stock_price_breadth_score_data_rating'] = data['stock_price_breadth']['data'][0]['rating']

        fear_greed_dict['put_call_options_score'] = round(data['put_call_options']['score'], 2)
        fear_greed_dict['put_call_options_rating'] = data['put_call_options']['rating']
        fear_greed_dict['put_call_options_score_data'] = round(data['put_call_options']['data'][0]['y'], 2)
        fear_greed_dict['put_call_options_score_data_rating'] = data['put_call_options']['data'][0]['rating']

        fear_greed_dict['market_volatility_vix_score'] = round(data['market_volatility_vix']['score'], 2)
        fear_greed_dict['market_volatility_vix_rating'] = data['market_volatility_vix']['rating']
        fear_greed_dict['market_volatility_vix_data'] = round(data['market_volatility_vix']['data'][0]['y'], 2)
        fear_greed_dict['market_volatility_vix_data_rating'] = data['market_volatility_vix']['data'][0]['rating']

        fear_greed_dict['market_volatility_vix_50_score'] = round(data['market_volatility_vix_50']['score'], 2)
        fear_greed_dict['market_volatility_vix_50_rating'] = data['market_volatility_vix_50']['rating']
        fear_greed_dict['market_volatility_vix_50_data'] = round(data['market_volatility_vix_50']['data'][0]['y'], 2)
        fear_greed_dict['market_volatility_vix_50_data_rating'] = data['market_volatility_vix_50']['data'][0]['rating']

        fear_greed_dict['junk_bond_demand_score'] = round(data['junk_bond_demand']['score'], 2)
        fear_greed_dict['junk_bond_demand_rating'] = data['junk_bond_demand']['rating']
        fear_greed_dict['junk_bond_demand_score_data'] = round(data['junk_bond_demand']['data'][0]['y'], 2)
        fear_greed_dict['junk_bond_demand_score_data_rating'] = data['junk_bond_demand']['data'][0]['rating']

        fear_greed_dict['safe_haven_demand_score'] = round(data['safe_haven_demand']['score'], 2)
        fear_greed_dict['safe_haven_demand_rating'] = data['safe_haven_demand']['rating']
        fear_greed_dict['safe_haven_demand_score_data'] = round(data['safe_haven_demand']['data'][0]['y'], 2)
        fear_greed_dict['safe_haven_demand_score_data_rating'] = data['safe_haven_demand']['data'][0]['rating']

        fear_greed_list.append(fear_greed_dict)

    # Create a dataframe
    df = pd.DataFrame(fear_greed_list)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.set_index('timestamp')
    df = df.sort_index()
    
    # write the data to a csv file
    with open(f'{dest_folder}/{file_name}', 'w') as f:
        df.to_csv(f)

    return df

get_fear_greed_index(date='2023-03-18', dest_folder='/Users/lohithyelamanchi/Trading/data/fear_and_greed', file_name='fear_greed_index.csv')