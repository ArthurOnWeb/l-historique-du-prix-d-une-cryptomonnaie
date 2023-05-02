import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Cryptocurrency:
    """Classe qui représente une cryptomonnaie
    """

    def __init__(self, symbol) -> None:
        self.symbol = symbol
        self.whitepaper = None
        self.name = None

    def get_price(self, interval, start, end):
        """Méthode qui permet de récupérer le prix d'ouverture, le plus haut, le plus bas et de fermeture de la cryptomonnaie dans le marché futures de l'échange Bybit durant l'interval choisi entre deux dates  dans une limite de 1 à 200 intervales 
        (!! 120 requests per second for 5 consecutive seconds maximum)
        Args:
            interval (string): interval de temps entre deux données (Kline interval. 1,3,5,15,30,60,120,240,360,720,D,M,W)
            start (integer): timestamp de la date de départ
            end (interger): timestamp de la date de fin
            limit (integer): nombre de données demandées (max 200)
        """
        url = f"https://api-testnet.bybit.com/v5/market/mark-price-kline?category=linear&symbol={self.symbol}USDT&interval={interval}&start={start}&end={end}"

        payload = {}
        headers = {}
        response = requests.request(
            "GET", url, headers=headers, data=payload).json()
        new_response = {}
        for data in response["result"]["list"]:
            new_response[data[0]] = {
                "symbol": response["result"]["symbol"],
                "open": data[1],
                "high": data[2],
                "low": data[3],
                "close": data[4]
            }

        return new_response

    def get_name_and_whitepaperlink(self):
        """Permet de récupérer le nom de la cryptomonnaie et de récupérer le lien du whitepaper de la cryptomonnaie

        Returns:
            list: nom de la cryptomonnaie et lien du whitepaper
        """
        # je récupère les informations sur le site coinmarketcap
        # je recherche la cryptomonnaie
        driver = webdriver.Chrome()
        driver.get(f'https://coinmarketcap.com/')
        elem = driver.find_element(
            By.CLASS_NAME, "sc-aef7b723-0.fKbUaI")
        elem.click()
        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'sc-2be9c14-3.gNiGam.desktop-input')))
        elem = driver.find_element(
            By.CLASS_NAME, 'sc-2be9c14-3.gNiGam.desktop-input')
        elem.clear()
        elem.send_keys(self.symbol)
        wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'sc-4984dd93-0.eZFtOL')))
        # je rajoute une seconde car il y a plusieurs éléments de cette classe, je veux le premier mais rarement un autre apparaît avant le premier
        time.sleep(1)
        elem = driver.find_element(By.CLASS_NAME, 'sc-4984dd93-0.eZFtOL')
        elem.click()
        # une fois la page de la cryptomonnaie atteinte, je récupère mes deux informations
        wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'sc-1d5226ca-1.fLa-dNu')))
        name = driver.find_element(
            By.CLASS_NAME, 'sc-1d5226ca-1.fLa-dNu').text
        self.name = name
        try:
            # find a child element
            child_element = driver.find_element(By.XPATH,
                                                "//div[text()='Whitepaper']")
            # find the parent element using XPath
            parent_element = child_element.find_element(By.XPATH, (".."))
            # get the href attribute
            href = parent_element.get_attribute("href")

            self.whitepaper = href
        except:
            self.whitepaper = "None"
        result = dict()
        result["name"] = self.name
        result["whitepaperLink"] = self.whitepaper
        return result


if __name__ == '__main__':
    # tests
    Bitcoin = Cryptocurrency('BTC')
    # print(datetime.strptime(
    #     "2023-04-01", "%Y-%m-%d").timestamp(), datetime.now())
    # print(Bitcoin.get_price('D', int(datetime.strptime("2023-04-01 22:00:00", "%Y-%m-%d %H:%M:%S").timestamp())*1000,
    #                         int(datetime.now().timestamp())*1000))
