import os
import requests
from binance.client import Client
from dotenv import load_dotenv
import pandas as pd
import mplfinance as mpf
import matplotlib
matplotlib.use('SVG')


load_dotenv()
pd.set_option('display.width', 320)
pd.set_option('display.max_columns',20)


api_key = os.getenv('API_KEY')
secret_key = os.getenv('SECRET_KEY')
base_url = 'https://api.binance.com'

client = Client(api_key, secret_key)


def make_graph(coin: str, days: int) -> None:
    historical = client.get_historical_klines(coin, Client.KLINE_INTERVAL_1DAY, '1 Jan 2011')
    historical_df = pd.DataFrame(historical)
    historical_df.columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume',
                             'Number of Trades', 'TB Base Volume', 'TB Quote Volume', 'Ignore']

    numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume',  'Quote Asset Volume',
                       'TB Base Volume', 'TB Quote Volume']

    historical_df[numeric_columns] = historical_df[numeric_columns].apply(pd.to_numeric, axis=1)
    historical_df['Open Time'] = pd.to_datetime(historical_df['Open Time']/1000, unit='s')
    historical_df['Close Time'] = pd.to_datetime(historical_df['Close Time']/1000, unit='s')

    mpf.plot(historical_df.set_index('Close Time').tail(days), type='candle', style="charles", savefig='testsave.png',
                                                               title=f'{coin} Last {days} Days')


def get_crypto_data(message: str) -> dict:
    avg_url = '/api/v3/avgPrice'
    params = {'symbol': message}
    response = requests.get(base_url+avg_url, params)
    return response.json()
