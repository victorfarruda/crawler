import csv
import json
import logging
import time

from bs4 import BeautifulSoup
from decouple import config
from selenium import webdriver
from selenium.webdriver.common.by import By

from choices import Fields, XPATH_REGION

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class CrawlerFinanceYahoo:
    def __init__(self, region):
        logging.info('CRIANDO OBJETO DE CRAWLER')
        self.region = region
        self.driver = webdriver.Chrome(chrome_options=self.get_options())
        self.driver.get("https://finance.yahoo.com/screener/new")

    def get_options(self):
        logging.info('GET OPTIONS')
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-dev-shm-usage')
        return chrome_options

    def login(self):
        logging.info('LOGIN DE USUARIO')
        signin = self.driver.find_element('id', 'header-signin-link')
        signin.click()
        logging.info('LOGIN DE USUARIO 2')
        time.sleep(5)

        login_username = self.driver.find_element('id', 'login-username')
        login_username.click()
        time.sleep(5)

        # username
        USERNAME_LOGIN = config('USERNAME_LOGIN', 'victorarruda2023@yahoo.com')
        login_username.send_keys(USERNAME_LOGIN)
        login_username.submit()
        time.sleep(5)

        # password
        login_password = self.driver.find_element('id', 'login-passwd')
        PASSWORD_LOGIN = config('PASSWORD_LOGIN', 'NovaSenha123!!')
        login_password.send_keys(PASSWORD_LOGIN)

        # logar
        login_id = self.driver.find_element('id', 'login-signin')
        login_id.click()

        time.sleep(5)

    def click_element(self, xpath):
        logging.info(f'GET ELEMENT {xpath}')
        element = self.driver.find_element(By.XPATH, xpath)
        element.click()
        time.sleep(5)

    def process_tbody(self, tbody):
        logging.info('PROCESSAR TBODY')
        new_list = []
        for tr in tbody:
            new_tr = {}
            for val, td in enumerate(tr):
                if val == Fields.SYMBOL.value:
                    new_tr['symbol'] = td.text
                elif val == Fields.NAME.value:
                    new_tr['name'] = td.text
                elif val == Fields.PRICE.value:
                    new_tr['price(intraday)'] = td.text
            new_list.append(new_tr)
        return new_list

    def create_csv(self, new_list):
        logging.info('CRIAR CSV')
        PATH_SAVE = config('PATH_SAVE', '')
        with open(f'{PATH_SAVE}{self.region}.csv', 'w') as csvfile:
            csv.writer(csvfile, delimiter=';').writerow(['name', 'symbol', 'price(intraday)'])
            for item in new_list:
                csv.writer(csvfile, delimiter=';').writerow([
                    item.get('name'),
                    item.get('symbol'),
                    item.get('price(intraday)')
                ])

    def process_table(self):
        logging.info('PROCESSAR TABELA')
        # pega corpo de tabela
        XPATH = '//*[@id="scr-res-table"]/div[1]/table/tbody'
        table = self.driver.find_element(By.XPATH, XPATH)
        html_table = table.get_attribute('innerHTML')
        time.sleep(5)
        table_body = BeautifulSoup(html_table, "html.parser")

        new_list = self.process_tbody(table_body)

        self.create_csv(new_list)
        self.create_json(new_list)

        self.driver.close()

    def create_json(self, new_list):
        logging.info('CRIAR JSON')
        json_object = json.dumps(new_list, indent=4)
        PATH_SAVE = config('PATH_SAVE', '')
        with open(f"{PATH_SAVE}{self.region}.json", "w") as outfile:
            outfile.write(json_object)

    def select_new_region(self):
        logging.info('SELECIONAR NOVA REGIÃO')
        xpath = XPATH_REGION.get(self.region)
        logging.info(f'GET ELEMENT {xpath}')
        element = self.driver.find_element(By.XPATH, xpath)
        self.driver.execute_script("arguments[0].click();", element)

        # if not element.is_selected():
        #     element.sel
        time.sleep(5)

    def run(self):
        logging.info('PREPARANDO PARA LOGIN')
        self.login()

        # remove region
        self.click_element('//*[@id="screener-criteria"]/div[2]/div[1]/div[1]/div[1]/div/div[2]/ul/li[1]/button')

        # abre para selecionar region
        self.click_element('//*[@id="screener-criteria"]/div[2]/div[1]/div[1]/div[1]/div/div[2]/ul/li/div/div[1]/span')

        # seleciona nova region
        time.sleep(5)
        self.select_new_region()

        # carrega tabela
        self.click_element('//*[@id="screener-criteria"]/div[2]/div[1]/div[3]/button[1]')

        self.process_table()
