import requests

base_url = 'https://api.binance.com'


def get_crypto_data(message: str) -> dict:
    avg_url = '/api/v3/avgPrice'
    params = {'symbol': message}
    response = requests.get(base_url+avg_url, params)
    return response.json()
