import asyncio

import pyinjective
from pyinjective.async_client import AsyncClient
from pyinjective.constant import Network

import importlib.resources as pkg_resources
import configparser
import requests
import json
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

async def price(base, quote):
    if base == "WETH":
        base = "ETH"
    if base =="USDT":
        return float(1)
    else:

        network = Network.mainnet()
        client = AsyncClient(network, insecure=False)
        oracle_type = 'BandIBC'
        oracle_scale_factor = 0
        oracle_prices = await client.get_oracle_prices(
            base_symbol=base,
            quote_symbol=quote,
            oracle_type=oracle_type,
            oracle_scale_factor=oracle_scale_factor
        )
        return round(float(oracle_prices.price), 2)

def get_denom(peggy):
    denoms_mainnet = pkg_resources.read_text(pyinjective, "denoms_mainnet.ini")
    network_config = configparser.RawConfigParser()
    network_config.read_string(denoms_mainnet)
    for peggy_id in network_config.sections():
        id = network_config[peggy_id].get('peggy_denom')
        if peggy == id:
            return float(network_config[peggy_id].get('decimals')), peggy_id

def auction_pending():
    url = " https://lcd.injective.network/injective/exchange/v1beta1/exchange/subaccountDeposits?subaccount_id=0x1111111111111111111111111111111111111111111111111111111111111111"
    r = requests.get(url)
    auction = json.loads(r.text)
    USDT_amount = float(auction["deposits"]["peggy0xdAC17F958D2ee523a2206206994597C13D831ec7"]["total_balance"])
    USDT_dec = float(get_denom("peggy0xdAC17F958D2ee523a2206206994597C13D831ec7")[0])
    USDT = round(USDT_amount/pow(10, USDT_dec), 2)
    return USDT

def get_market_id(market_form, base, quote):
    denoms_mainnet = pkg_resources.read_text(pyinjective, "denoms_mainnet.ini")
    network_config = configparser.RawConfigParser()
    network_config.read_string(denoms_mainnet)
    pair = base + "/" + quote

    for market_id in network_config.sections():
        description = network_config[market_id].get('description')

        if description:
            information = description.replace("'", "").split(" ")
            market_type = information[1]
            symbol = information[2]
            if market_type == market_form and symbol == pair:
                return market_id

def get_ob(market_id, type, base, quote):
    if type == 'Derivative':
        url = "https://lcd.injective.network/injective/exchange/v1beta1/derivative/orderbook/" + market_id + "?limit=30"
    else:
        url = "https://lcd.injective.network/injective/exchange/v1beta1/spot/orderbook/" + market_id + "?limit=20"

    r = requests.get(url)

    data = json.loads(r.text)

    data["buys_price_level"]
    data["sells_price_level"]

    denoms_mainnet = pkg_resources.read_text(pyinjective, "denoms_mainnet.ini")
    network_config = configparser.RawConfigParser()
    network_config.read_string(denoms_mainnet)
    base_dec = 10**int(network_config[market_id].get('base'))
    quote_dec = 10**int(network_config[market_id].get('quote'))

    if type == 'Spot':
        price_const = quote_dec / base_dec
        quant_const = base_dec
    else:
        price_const = quote_dec
        quant_const = base_dec


    x_bids = []
    x_ask = []

    for i in range(len(data["buys_price_level"])):
        buy_df = {
                "price" : round(float(data["buys_price_level"][i]["p"]) / price_const, 2),
                "quantity" : round(float(data["buys_price_level"][i]["q"]) / quant_const, 2),
                "side" : "bids"
        }

        x_bids.append(buy_df)

    for i in range(len(data["sells_price_level"])):
        sell_df = {
            "price" : round(float(data["sells_price_level"][i]["p"]) / price_const, 2),
            "quantity" : round(float(data["sells_price_level"][i]["q"]) / quant_const, 2),
            "side" : "asks"
        }

        x_ask.append(sell_df)

    df_bids = pd.DataFrame(x_bids)
    df_asks = pd.DataFrame(x_ask)

    df_summary = pd.concat([df_bids, df_asks], axis=0)

    fig, ax = plt.subplots()
    ax.set_title(f"Injective: {base}/{quote} {type} Depth")
    sns.ecdfplot(x="price", weights="quantity", stat="count", 
                complementary=True, data=df_summary.query("side == 'bids'"), 
                color="green", ax=ax)
    sns.ecdfplot(x="price", weights="quantity", stat="count", 
                data=df_summary.query("side == 'asks'"), color="red", 
                ax=ax)
    ax.set_xlabel("Price")
    ax.set_ylabel("Quantity")

    plt.savefig(f"tmp/{base}_{quote}_{type}.png", dpi=300)

def get_volume():
    url = "https://api.injective.network/api/chronos/v1/derivative/market_summary_all?resolution=24h"

    r = requests.get(url)

    data = json.loads(r.text)  
    volume = 0

    for i in range(len(data)):
        volume += float(data[i]["volume"])
    volume_tidy=round(volume,2)
    volume_clean= "{:,}".format(volume_tidy)
    return volume_clean


if __name__ == '__main__':
    # asyncio.run(price("WETH", "USDT"))
    # get_denom("peggy0xdAC17F958D2ee523a2206206994597C13D831ec7")
    # print(auction_pending())
    get_volume()