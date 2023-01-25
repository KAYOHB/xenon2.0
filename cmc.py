from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


def mcof(quote):
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    parameters = {
    'symbol':f'INJ,{quote}',
    'convert':'USD'
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'f886956b-65e1-4b28-ba9c-b0a3a93c6152',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        mc_inj = float(data['data']['INJ'][0]["quote"]["USD"]["market_cap"])
        mc_quote = float(data['data'][quote][0]["quote"]["USD"]["market_cap"])
        price = float(data['data']['INJ'][0]["quote"]["USD"]["price"])
        val = round(price* mc_quote/mc_inj, 2)
        return val
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

class CMC():
    pass

if __name__ == "__main__":
    print(mcof('BTC'))