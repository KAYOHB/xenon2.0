import asyncio
import os
from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
import requests
import json
import importlib.resources as pkg_resources
import configparser
import pyinjective
import telebot
from aiohttp import web
import logging
import ssl


from utils import price, get_denom, auction_pending, get_ob, get_market_id, get_volume
from cmc import mcof

load_dotenv()
API_TOKEN = os.getenv("api_key")
WEBHOOK_HOST = 'xenon3.ddns.net'
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr
WEBHOOK_SSL_CERT = 'ssl/webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = 'ssl/webhook_pkey.pem'  # Path to the ssl private key
WEBHOOK_URL_BASE = "https://{}:{}".format(WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(API_TOKEN)

# Process webhook calls
async def handle(request):
    if request.match_info.get('token') == bot.token:
        request_body_dict = await request.json()
        update = telebot.types.Update.de_json(request_body_dict)
        asyncio.ensure_future(bot.process_new_updates([update]))
        return web.Response()
    else:
        return web.Response(status=403)


#Load bot api_key
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
bot = AsyncTeleBot(API_TOKEN)

@bot.message_handler(commands=["tokenomics"])
async def tokenomics(message):
    with open("token.png", 'rb') as file:
        info = file.read()
    await bot.send_photo(chat_id= message.chat.id, photo=info, caption="Source: https://injective.notion.site/injective/Injective-INJ-e1f0aff38d5546f5be9f47efab5b972b\n\n"
    "ELI - 0 IQ:\n\nMax Supply: 100,000,000 $INJ\n\n"
    "The token is naturally inflationary due to its Proof-of-Stake consensus mechanism. Tokens are minted to reward validators/delegators.\n\n"
    "But before your bitch ass begins to sweat, please allow your sorry ass know that there is a weekly buy back and burn event where 60% of exchange fees are auctioned off. " 
    "Bids for the auction are in $INJ. The winner's tokens are then burned\n\n"
    "Example, if we use the current $INJ price of $1.70; current auction basket of $10,388.64 and assume UEMRE3 is bidding then:\n\n"
    "10,388.64/$1.70 = 6110 $INJ tokens burned\n\n"
    "tlrd: The higher the volume on the exchange, the higher the burn.\n\n"
    , reply_to_message_id=message)

@bot.message_handler(commands=["tokenomi_turk"])
async def tokenomics(message):
    await bot.reply_to(message, text="Source: https://injective.notion.site/injective/Injective-INJ-e1f0aff38d5546f5be9f47efab5b972b\n\n"
    "INJ injectivin yerel ve yard??mc?? tokendir. INJ s??n??rl?? bir y??neti??im varl??????d??r PoS a???? i??erisinde ger??ekle??tirilen Staking ve a????k artt??rma ??cretleri yak??l??r injectivedeki yak??lan a????k artt??rmalar dapplerden toplanan t??m ??cretlerin %60??ndan beri her hafta bir geri sat??n alma ve yak??m mekanizmas?? ile a????k artt??rmaya ????k??yor bu ??zellik ile injectivenin arz??n??n zaman i??erisinde ??nemli ??l????de azalmas??na yard??mc?? oluyor injectivenin yak??m a????k artt??rmas?? t??m injective ekosistemine yard??mc?? olmas?? bak??m??ndan e??sizdir ??u anda injective sekt??rdeki en y??ksek token yakma oran??na sahip injective i??in hedeflenen kullan??m ama??lar??na say??lanlar ile s??n??rl?? olmamak kayd??yla: protokol y??netimi ,( injective hakk??nda ??e??itli oylamalara kat??lma ) dapp de??erine ula??ma , PoS g??venli??i , geli??tirici te??vikleri ve stake ??zelli??i t??m bu kullan??m ama??lar?? ile ilgili daha detayl?? bilgiye hep beraber a??a????da bakal??m ????\n\n"
    "PROTOKOL Y??NET??M??: inj token injectivenin zincir y??kseltmeleri de dahil injectivenin her bile??enini y??netme imkan?? sunar ana a?? lansman??ndan bu yana injective toplulu??u aktif olarak y??neti??ime bir dao oylama sistemi ile t??m tekliflere katk??da bulunuyorlar kapsaml?? bilgi bulunan y??neti??im sayfas?? burada\n\n"
    "PROTOKOL FEE ??CRET??NE ULA??MAK: dapplerden elde edilen t??m ??cretlerin %60 ?? zincir ??zerinden sat??n al??n??r geri al??nan tutar a????k artt??rma ile yak??l??r bu a????k artt??rma i??lemi injectivenin deflasyonist yap??s??n?? korumak i??in yap??l??r detayl?? yak??m sayfas?? burada\n\n" 
    "TENDERM??NT BAZLI POS G??VENL?????? : inj injectivenin g??venli??ini sa??lamak i??in kullan??l??r proof of stake ( hisse kan??t??na dayal?? ) mekanizmas??n?? kullan??r validat??rler ve delegat??rler stakinge beraber kat??labilirler\n\n"
    "GEL????T??R??C?? TE??V??KLER??: ??njective ??zerine kurulu dapplerde kullan??c?? taraf??ndan olu??turulan ??cretlerin %40 ?? injective ??zerinde in??a eden yeni geli??tiricileri te??vik etmeye y??neliktir ve bu da injectivede giderek ilerleyen bir in??a a??amas?? olu??turur\n\n"
    "EKSTRA: TENDERM??NT UYGULAMALARI HERHANG?? B??R YAZILIM D??L??NDE YAZMAYA ??MKAN TANIYAN BLOKZ??NC??RLER YARATMAYA Y??NEL??K A??IK KAYNAKLI YAZILIMDIR")

@bot.message_handler(commands=["dapps"])
async def tokenomics(message):
    await bot.reply_to(message, "Trade on any of the following Injective exchange dApps:\n\n"
    "INJ Dojo - https://injdojo.exchange/markets\ The official dojo exchange dapp built by nINJas for nINJas\n\n"
    "Frontrunner - https://app.getfrontrunner.com/ A sports betting dApp built on Injective\n\n"
    "Helix - https://helixapp.com/ - The official exchange dApp built by the Injective Labs team\n\n"
    "Wavely - https://www.wavely.app/ - An exchange dapp built by a nINJa, awesome UI!\n\n"
    "QWERTY - https://qwerty.exchange/ - new exchange dApp looking to revolutionise the standard of exchange dApps on Injective. Look out for them!\n\n"
    "Dexterium - https://dexterium.exchange/ - home of the very first guilds.")

@bot.message_handler(commands=["auction"])
async def send_auction(message):
    url = "https://lcd.injective.network/injective/auction/v1beta1/basket"
    r = requests.get(url)
    auctions = json.loads(r.text)
    bidder = auctions["highestBidder"][:3] + "..." + auctions["highestBidder"][-6:]
    bid = round(float(auctions["highestBidAmount"])/pow(10, 18), 2)
    bid_clean ="{:,}".format(bid)
    inj_price = await price("INJ", "USDT")
    auction = []
    for i in range(len(auctions["amount"])):
        basket = {
            "name" : get_denom(auctions["amount"][i]["denom"]),
            "amount" : float(auctions["amount"][i]["amount"])
            /pow(10, float(get_denom(auctions["amount"][i]["denom"])[0])),
            "value" : round(float(auctions["amount"][i]["amount"])
            /pow(10, float(get_denom(auctions["amount"][i]["denom"])[0]))
            *await price(get_denom(auctions["amount"][i]["denom"])[1], "USDT"), 2)
        }
        auction.append(basket)
    basket = 0
    for i in range(len(auction)):
        basket += auction[i]["value"]
    inj_equ = round(basket / inj_price, 2)
    profit = round(basket - inj_equ, 2)
    bid_worth = bid*inj_price
    basket_clean = "{:,}".format(basket)
    inj_equ_clean = "{:,}".format(inj_equ)
    profit_clean = "{:,}".format(profit)
    bid_worth_clean = "{:,}".format(bid_worth)
    await bot.reply_to(message, text=f"Current Basket: ${basket_clean} ??? {inj_equ_clean} $INJ\nTop Bidder: {bidder}\nBid Amount: {bid_clean} $INJ ??? ${bid_worth_clean}\nCurrent Profit: ${profit_clean}\n\nMore information at:\nhttps://hub.injective.network/auction/")

@bot.message_handler(commands=["A????k_artt??rma"])
async def send_auction(message):
    url = "https://lcd.injective.network/injective/auction/v1beta1/basket"
    r = requests.get(url)
    auctions = json.loads(r.text)
    bidder = auctions["highestBidder"][:3] + "..." + auctions["highestBidder"][-6:]
    bid = round(float(auctions["highestBidAmount"])/pow(10, 18))
    inj_price = await price("INJ", "USDT")
    auction = []
    for i in range(len(auctions["amount"])):
        basket = {
            "name" : get_denom(auctions["amount"][i]["denom"]),
            "amount" : float(auctions["amount"][i]["amount"])
            /pow(10, float(get_denom(auctions["amount"][i]["denom"])[0])),
            "value" : round(float(auctions["amount"][i]["amount"])
            /pow(10, float(get_denom(auctions["amount"][i]["denom"])[0]))
            *await price(get_denom(auctions["amount"][i]["denom"])[1], "USDT"), 2)
        }
        auction.append(basket)
    basket = 0
    for i in range(len(auction)):
        basket += auction[i]["value"]
    inj_equ = round(basket / inj_price)
    profit = round(basket - inj_equ)
    bid_worth = round(bid*inj_price)
    basket_clean = "{:,}".format(round(basket)).replace(',','.')
    inj_equ_clean = "{:,}".format(inj_equ).replace(',','.')
    profit_clean = "{:,}".format(profit).replace(',','.')
    bid_worth_clean = "{:,}".format(bid_worth).replace(',','.')
    bid_clean ="{:,}".format(bid).replace(',','.')
    await bot.reply_to(message, text=f"Mevcut sepet de??eri ${basket_clean} ??? {inj_equ_clean} $INJ\nEn y??ksek teklif: {bidder}\nVerilen teklif tutar {bid_clean} $INJ ??? ${bid_worth_clean}\nMevcut k??r: ${profit_clean}\n\nDaha fazla bilgi i??in ????:\nhttps://hub.injective.network/auction/")

@bot.message_handler(commands=["subasta"])
async def send_auction(message):
    url = "https://lcd.injective.network/injective/auction/v1beta1/basket"
    r = requests.get(url)
    auctions = json.loads(r.text)
    bidder = auctions["highestBidder"][:3] + "..." + auctions["highestBidder"][-6:]
    bid = round(float(auctions["highestBidAmount"])/pow(10, 18))
    inj_price = await price("INJ", "USDT")
    auction = []
    for i in range(len(auctions["amount"])):
        basket = {
            "name" : get_denom(auctions["amount"][i]["denom"]),
            "amount" : float(auctions["amount"][i]["amount"])
            /pow(10, float(get_denom(auctions["amount"][i]["denom"])[0])),
            "value" : round(float(auctions["amount"][i]["amount"])
            /pow(10, float(get_denom(auctions["amount"][i]["denom"])[0]))
            *await price(get_denom(auctions["amount"][i]["denom"])[1], "USDT"), 2)
        }
        auction.append(basket)
    basket = 0
    for i in range(len(auction)):
        basket += auction[i]["value"]
    inj_equ = round(basket / inj_price)
    profit = round(basket - inj_equ)
    bid_worth = round(bid*inj_price)
    basket_clean = "{:,}".format(round(basket)).replace(',','.')
    inj_equ_clean = "{:,}".format(inj_equ).replace(',','.')
    profit_clean = "{:,}".format(profit).replace(',','.')
    bid_worth_clean = "{:,}".format(bid_worth).replace(',','.')
    bid_clean ="{:,}".format(bid).replace(',','.')
    await bot.reply_to(message, text=f"Canasta Actual: ${basket_clean} ??? {inj_equ_clean} $INJ\nMejor Postor: {bidder}\nCantidad de la Oferta: {bid_clean} $INJ ??? ${bid_worth_clean}\nGanancia Actual: ${profit_clean}\n\nM??s informaci??n en:\nhttps://hub.injective.network/auction/")

@bot.message_handler(commands=["pendingauction"])
async def pending(message):
    auction = auction_pending()
    await bot.reply_to(message, text=f"The value of next week's pending auction is:\n\n${auction}\n\n"
    "Please note, the value of this basket only consists of USDT.")

@bot.message_handler(commands=["m??zayede_vakti_bekleniyor"])
async def pending(message):
    auction = auction_pending()
    await bot.reply_to(message, text=f"Gelecek haftan??n ger??ekle??ecek olan m??zayedenin de??eri:\n\n${auction}\n\n"
    "L??tfen dikkat bu sepetin de??eri sadece USDT???den olu??maktad??r.")

@bot.message_handler(commands=["injob"])
async def send_ob(message):
    denoms_mainnet = pkg_resources.read_text(pyinjective, "denoms_mainnet.ini")
    network_config = configparser.RawConfigParser()
    network_config.read_string(denoms_mainnet)
    accepted = ["spot", "perp"]
    perp_base = ["BTC", "ETH", "BNB", "ATOM", "OSMO", "STX", "INJ"]
    request = message.text.split()
    if len(request) != 4:
        await bot.reply_to(message, f"incorrect request, should be of format 'injob base_denom quote_denom market_type")
        return False
    elif request[3].lower() not in accepted:
        await bot.reply_to(message, f"{request[3]} not recognised. Markets are either 'Perp' or 'Spot'")
        return False
    elif request[3].lower() == "spot" and request[1].upper() not in network_config.sections():
        await bot.reply_to(message, f"{request[1]} is not currently listed as a spot market base denom")
        return False
    elif request[3].lower() == "perp" and request[1].upper() not in perp_base:
        await bot.reply_to(message, f"{request[1]} is not currently listed as a perp market base denom")
        return False
    elif request[2].upper() not in network_config.sections():
        await bot.reply_to(message, f"{request[2]} is not currently listed as any market's quote denom")
        return False
    else:
        base_denom = message.text.split()[1].upper()
        quote_denom = message.text.split()[2].upper()
        if message.text.split()[3].lower() != 'perp':
            market_type = 'Spot'
        else:
            market_type = 'Derivative'

        ob = get_market_id(market_type, base_denom, quote_denom)

        get_ob(ob, market_type, base_denom, quote_denom)

        with open(f'tmp/{base_denom}_{quote_denom}_{market_type}.png', 'rb') as file:
            data = file.read()
        await bot.send_photo(chat_id= message.chat.id, photo = data, caption = f'{base_denom}/{quote_denom} {market_type} OB, brought to you by Xenon.\nSponsored by no one yet :|', reply_to_message_id=message)

@bot.message_handler(commands=["volume"])
async def pending(message):
    vol = get_volume()
    auction = auction_pending()
    await bot.reply_to(message, text=f"Total on-chain volume is currently:\n\n${vol}\n\nNext week's pending auction basket has accumulated:\n\n${auction}")

@bot.message_handler(commands=["mcof"])
async def mc(message):
    request = message.text.split()[1].upper()
    print(request)
    price_if = mcof(f'{request}')
    await bot.reply_to(message, text=f"if INJ had the Market Cap of {request}, then the price per token would be ${price_if} per token.")

async def shutdown(app):
    logger.info('Shutting down: removing webhook')
    await bot.remove_webhook()
    logger.info('Shutting down: closing session')
    await bot.close_session()

async def setup():
    # Remove webhook, it fails sometimes the set if there is a previous webhook
    logger.info('Starting up: removing old webhook')
    await bot.remove_webhook()
    # Set webhook
    logger.info('Starting up: setting webhook')
    await bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH, certificate=open(WEBHOOK_SSL_CERT, 'r'))
    app = web.Application()
    app.router.add_post('/{token}/', handle)
    app.on_cleanup.append(shutdown)
    return app

if __name__ == '__main__':
    # Build ssl context
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)
    # Start aiohttp server
    web.run_app(
        setup(),
        host=WEBHOOK_LISTEN,
        port=WEBHOOK_PORT,
        ssl_context=context,
    )

