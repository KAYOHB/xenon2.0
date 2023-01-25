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
API_TOKEN = os.getenv("api_key_test")
WEBHOOK_HOST = 'xenon3.ddns.net'
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr
WEBHOOK_SSL_CERT = '/home/kayo/projects/tg1/main/xenon2.0/ssl/webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = '/home/kayo/projects/tg1/main/xenon2.0/ssl/webhook_pkey.pem'  # Path to the ssl private key
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
    "INJ injectivin yerel ve yardımcı tokendir. INJ sınırlı bir yönetişim varlığıdır PoS ağı içerisinde gerçekleştirilen Staking ve açık arttırma ücretleri yakılır injectivedeki yakılan açık arttırmalar dapplerden toplanan tüm ücretlerin %60ından beri her hafta bir geri satın alma ve yakım mekanizması ile açık arttırmaya çıkıyor bu özellik ile injectivenin arzının zaman içerisinde önemli ölçüde azalmasına yardımcı oluyor injectivenin yakım açık arttırması tüm injective ekosistemine yardımcı olması bakımından eşsizdir şu anda injective sektördeki en yüksek token yakma oranına sahip injective için hedeflenen kullanım amaçlarına sayılanlar ile sınırlı olmamak kaydıyla: protokol yönetimi ,( injective hakkında çeşitli oylamalara katılma ) dapp değerine ulaşma , PoS güvenliği , geliştirici teşvikleri ve stake özelliği tüm bu kullanım amaçları ile ilgili daha detaylı bilgiye hep beraber aşağıda bakalım 👇\n\n"
    "PROTOKOL YÖNETİMİ: inj token injectivenin zincir yükseltmeleri de dahil injectivenin her bileşenini yönetme imkanı sunar ana ağ lansmanından bu yana injective topluluğu aktif olarak yönetişime bir dao oylama sistemi ile tüm tekliflere katkıda bulunuyorlar kapsamlı bilgi bulunan yönetişim sayfası burada\n\n"
    "PROTOKOL FEE ÜCRETİNE ULAŞMAK: dapplerden elde edilen tüm ücretlerin %60 ı zincir üzerinden satın alınır geri alınan tutar açık arttırma ile yakılır bu açık arttırma işlemi injectivenin deflasyonist yapısını korumak için yapılır detaylı yakım sayfası burada\n\n" 
    "TENDERMİNT BAZLI POS GÜVENLİĞİ : inj injectivenin güvenliğini sağlamak için kullanılır proof of stake ( hisse kanıtına dayalı ) mekanizmasını kullanır validatörler ve delegatörler stakinge beraber katılabilirler\n\n"
    "GELİŞTİRİCİ TEŞVİKLERİ: İnjective üzerine kurulu dapplerde kullanıcı tarafından oluşturulan ücretlerin %40 ı injective üzerinde inşa eden yeni geliştiricileri teşvik etmeye yöneliktir ve bu da injectivede giderek ilerleyen bir inşa aşaması oluşturur\n\n"
    "EKSTRA: TENDERMİNT UYGULAMALARI HERHANGİ BİR YAZILIM DİLİNDE YAZMAYA İMKAN TANIYAN BLOKZİNCİRLER YARATMAYA YÖNELİK AÇIK KAYNAKLI YAZILIMDIR")

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
    await bot.reply_to(message, text=f"Current Basket: ${basket_clean} ≈ {inj_equ_clean} $INJ\nTop Bidder: {bidder}\nBid Amount: {bid_clean} $INJ ≈ ${bid_worth_clean}\nCurrent Profit: ${profit_clean}\n\nMore information at:\nhttps://hub.injective.network/auction/")

@bot.message_handler(commands=["Açık_arttırma"])
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
    await bot.reply_to(message, text=f"Mevcut sepet değeri ${basket_clean} ≈ {inj_equ_clean} $INJ\nEn yüksek teklif: {bidder}\nVerilen teklif tutar {bid_clean} $INJ ≈ ${bid_worth_clean}\nMevcut kâr: ${profit_clean}\n\nDaha fazla bilgi için 👇:\nhttps://hub.injective.network/auction/")

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
    await bot.reply_to(message, text=f"Canasta Actual: ${basket_clean} ≈ {inj_equ_clean} $INJ\nMejor Postor: {bidder}\nCantidad de la Oferta: {bid_clean} $INJ ≈ ${bid_worth_clean}\nGanancia Actual: ${profit_clean}\n\nMás información en:\nhttps://hub.injective.network/auction/")

@bot.message_handler(commands=["pendingauction"])
async def pending(message):
    auction = auction_pending()
    await bot.reply_to(message, text=f"The value of next week's pending auction is:\n\n${auction}\n\n"
    "Please note, the value of this basket only consists of USDT.")

@bot.message_handler(commands=["müzayede_vakti_bekleniyor"])
async def pending(message):
    auction = auction_pending()
    await bot.reply_to(message, text=f"Gelecek haftanın gerçekleşecek olan müzayedenin değeri:\n\n${auction}\n\n"
    "Lütfen dikkat bu sepetin değeri sadece USDT’den oluşmaktadır.")

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

