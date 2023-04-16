import logging

from decouple import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

from src.crawler import CrawlerFinanceYahoo

if __name__ == '__main__':
    REGION = config('REGION', 'Brazil')
    logging.info('INICIANDO...')
    crawler = CrawlerFinanceYahoo(region=REGION)
    logging.info('CRAWLER CRIADO')
    crawler.run()
