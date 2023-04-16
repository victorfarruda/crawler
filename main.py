import logging
import sys

from decouple import config

from src.choices import XPATH_REGION
from src.crawler import CrawlerFinanceYahoo

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def main(region):
    logging.info(f'INICIANDO... NA REGIÃO "{region}"')
    crawler = CrawlerFinanceYahoo(region=region)
    logging.info('CRAWLER CRIADO')
    crawler.run()


if __name__ == '__main__':
    try:
        REGION = " ".join(sys.argv[1:]) if not sys.argv[1:] == [] else config('REGION', 'Brazil')
        region_xpath = XPATH_REGION.get(REGION)
        if region_xpath is None:
            raise Exception("REGIÃO NÃO PODE SER LOCALIZADA, VERIFIQUE SE DIGITOU CORRETAMENTE!!!")
        else:
            main(region=REGION)
    except Exception as e:
        logging.error(e)
