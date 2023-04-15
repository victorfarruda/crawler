import csv
import json
import time

from bs4 import BeautifulSoup
from decouple import config
from selenium import webdriver
from selenium.webdriver.common.by import By

from src.choices import Fields, XPATH_REGION
from src.settings import PATH_SAVE, logging


class CrawlerFinanceYahoo:
    def __init__(self, region):
        logging.info('CRIANDO OBJETO DE CRAWLER')
        self.region = region
        self.driver = None

    def get_options(self):
        logging.info('PEGAR OPÇÕES DE DRIVER')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        return chrome_options

    def get_driver(self):
        return webdriver.Chrome(chrome_options=self.get_options())

    def login(self):
        logging.info('LOGANDO USUARIO')
        signin = self.driver.find_element('id', 'header-signin-link')
        signin.click()
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

        logging.info('USUÁRIO LOGADO COM SUCESSO')
        time.sleep(5)

    def click_element(self, xpath):
        logging.info(f'CLICAR EM ELEMENTO {xpath}')
        element = self.driver.find_element(By.XPATH, xpath)
        element.click()
        time.sleep(5)

    def process_tbody(self, tbody):
        logging.info('PROCESSAR TBODY (DADOS)')
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
                else:
                    continue
            new_list.append(new_tr)
        return new_list

    def create_csv(self, new_list):
        logging.info('CRIAR CSV')
        with open(f'{PATH_SAVE}{self.region}.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(['name', 'symbol', 'price(intraday)'])
            for item in new_list:
                writer.writerow([item.get('name'), item.get('symbol'), item.get('price(intraday)')])

    def create_json(self, new_list):
        logging.info('CRIAR JSON')
        json_object = json.dumps(new_list, indent=4)
        with open(f"{PATH_SAVE}{self.region}.json", "w") as outfile:
            outfile.write(json_object)

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

    def load_page(self):
        self.driver = self.get_driver()
        self.driver.get("https://finance.yahoo.com/screener/new")

    def select_new_region(self):
        time.sleep(5)
        logging.info('SELECIONAR NOVA REGIÃO')
        xpath = XPATH_REGION.get(self.region)
        logging.info(f'CLICAR EM NOVA REGIÃO {xpath}')
        element = self.driver.find_element(By.XPATH, xpath)
        self.driver.execute_script("arguments[0].click();", element)
        time.sleep(5)

    def run(self):
        logging.info('***INICIANDO RASPAGEM DE DADOS***')
        self.load_page()

        logging.info('PREPARANDO PARA LOGAR')
        self.login()

        # remove region
        logging.info('REMOVER REGIÃO PADRÃO')
        self.click_element('//*[@id="screener-criteria"]/div[2]/div[1]/div[1]/div[1]/div/div[2]/ul/li[1]/button')

        # abre para selecionar region
        logging.info('CLICAR PARA SELECIONAR REGIÃO')
        self.click_element('//*[@id="screener-criteria"]/div[2]/div[1]/div[1]/div[1]/div/div[2]/ul/li/div/div[1]/span')

        # seleciona nova region
        self.select_new_region()

        # carrega tabela
        logging.info('CLICAR PARA CARREGAR TABELA')
        self.click_element('//*[@id="screener-criteria"]/div[2]/div[1]/div[3]/button[1]')

        self.process_table()
        logging.info('***RASPAGEM DE DADOS FINALIZADA COM SUCESSO***')
