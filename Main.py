import CryptoCurrency
import sqlite3 as sql
import requests
from datetime import datetime
import time


def get_crypto():
    """Récupères la liste des cryptomonnaies tradable sur le marché futures de Bybit
    (!! 120 requests per second for 5 consecutive seconds maximum)
    Returns:
        list:liste des cryptomonnaies
    """

    url = "https://api-testnet.bybit.com/v5/market/instruments-info?category=linear"

    payload = {}
    headers = {}

    response = requests.request(
        "GET", url, headers=headers, data=payload).json()
    baseCoins = []

    for crypto in response['result']['list']:
        if crypto['baseCoin'][:5] == '10000' and crypto['quoteCoin'] == 'USDT' and crypto['baseCoin'] not in baseCoins:
            # baseCoins += [crypto['baseCoin'][5:]]
            # non traité pour le moment
            pass
        elif crypto['baseCoin'][:4] == '1000' and crypto['quoteCoin'] == 'USDT' and crypto['baseCoin'] not in baseCoins:
            # baseCoins += [crypto['baseCoin'][4:]]
            # non traité pour le moment
            pass
        elif crypto['quoteCoin'] == 'USDT' and crypto['baseCoin'] not in baseCoins and crypto['baseCoin'] != 'LUNA2' and crypto['baseCoin'] != 'PEOPLE':
            # exception LUNA2 et PEOPLE à traiter
            baseCoins += [crypto['baseCoin']]

    return baseCoins


def get_price_history(interval, crypto):
    """renvoie un dicitonnaire qui permet de connaître le prix de la cryptomonnaie depuis l'apparition de son contrat futures sur l'échange de cryptomonnaie.


    Args:
        interval (string): interval de temps entre deux données (Kline interval. 1,3,5,15,30,60,120,240,360,720,D,M,W)
        crypto (CryptoCurrency): la crypto dont on veut le prix
    """
    listeDictionnaires = []
    listeDictionnaires.append(crypto.get_price(interval, 1500000000000,
                                               int(datetime.now().timestamp())*1000))
    lastTimestamps = list(listeDictionnaires[0].keys())
    lastTimestamps.sort()
    if len(lastTimestamps) < 200:
        return listeDictionnaires
    # intervalInTimestamp = int(lastTimestamps[2])-int(lastTimestamps[1])
    # jusqu'ici on a récupéré les 200 derniers timestamps
    compteur = 1
    while len(lastTimestamps) == 200:
        listeDictionnaires.append(crypto.get_price(
            interval, 1500000000000, int(lastTimestamps[0])))
        # il ne faut pas dépasser les 120 requetes par 5 secondes
        if compteur % 119 == 0:
            time.sleep(5)
        lastTimestamps = (list(listeDictionnaires[compteur].keys()))
        lastTimestamps.sort()
        compteur += 1
    print(listeDictionnaires)
    return listeDictionnaires


if __name__ == "__main__":
    # fonctionnement normal
    print(get_crypto())
    # cryptos = get_crypto()
    # conn = sql.connect("cryptoDatabase.db")
    # curs = conn.cursor()
    # curs.execute("DROP TABLE IF EXISTS Crypto")
    # curs.execute(
    #     "CREATE TABLE  Crypto (nom VARCHAR, symbol VARCHAR PRIMARY KEY, whitepaperlink VARCHAR)")
    # curs.execute("DROP TABLE IF EXISTS Prix")
    # curs.execute(
    #     "CREATE TABLE  Prix (symbol VARCHAR, date VARCHAR, open FLOAT, high FLOAT, low FLOAT, close FLOAT,PRIMARY KEY (symbol, date),FOREIGN KEY (symbol) REFERENCES Crypto(symbol))")
    # cryptoCurrencies = []
    # for crypto in cryptos:
    #     cryptoCurrencies += [CryptoCurrency.Cryptocurrency(crypto)]
    # for crypto in cryptoCurrencies:
    #     infos = crypto.get_name_and_whitepaperlink()
    #     # l'interval choisi ici est hebdomadaire si on veut plus de précision, on peut prendre un plus petit interval
    #     price_history = get_price_history(
    #         "W", crypto)
    #     curs.execute("INSERT INTO Crypto(nom,symbol,whitepaperlink) VALUES (?,?,?)",
    #                  (infos["name"], crypto.symbol, infos["whitepaperLink"]))
    #     conn.commit()
    #     for prices in price_history:
    #         timestamps = list(prices.keys())
    #         for date in timestamps:
    #             curs.execute("INSERT INTO Prix(symbol,date,open,high,low,close) VALUES (?,?,?,?,?,?)",
    #                          (crypto.symbol, datetime.fromtimestamp(int(date)/1000), prices[date]["open"], prices[date]["high"], prices[date]["low"], prices[date]["close"]))
    #             conn.commit()
    # conn.commit()
    # conn.close()

    # test

    # nft = CryptoCurrency.Cryptocurrency('EOS')
    # print(get_price_history("D", nft))
    # bitcoin = CryptoCurrency.Cryptocurrency("BTC")
    # get_price_history("D", bitcoin)
    # infos = bitcoin.get_name_and_whitepaperlink()
    # conn = sql.connect("cryptoDatabase.db")
    # curs = conn.cursor()
    # curs.execute("DROP TABLE IF EXISTS Crypto")
    # curs.execute(
    #     "CREATE TABLE  Crypto (nom VARCHAR PRIMARY KEY, symbole VARCHAR, whitepaperlink VARCHAR)")
    # curs.execute(
    #     "INSERT INTO Crypto(nom,symbole,whitepaperlink) VALUES (?,?,?)", (infos["name"], bitcoin.symbol, infos["whitepaperLink"]))
    # conn.commit()
    # conn.close()
