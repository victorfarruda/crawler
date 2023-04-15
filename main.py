from decouple import config
from src.settings import logging

from src.crawler import CrawlerFinanceYahoo


if __name__ == '__main__':
    REGION = config('REGION', 'Brazil')
    logging.info('INICIANDO...')
    crawler = CrawlerFinanceYahoo(region=REGION)
    logging.info('CRAWLER CRIADO')
    crawler.run()
