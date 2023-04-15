from decouple import config
from settings import logging

from crawler import CrawlerFinanceYahoo


if __name__ == '__main__':
    REGION = config('REGION', 'Brazil')
    logging.info('INICIANDO...')
    crawler = CrawlerFinanceYahoo(region=REGION)
    logging.info('CRAWLER CRIADO')
    crawler.run()
