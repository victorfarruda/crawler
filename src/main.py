import logging

from decouple import config

from crawler import CrawlerFinanceYahoo

logging.basicConfig(level=logging.INFO, filename="programa.log", format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == '__main__':
    REGION = config('REGION', 'Brazil')
    logging.info('INICIOU O PROGRAMA')
    crawler = CrawlerFinanceYahoo(region=REGION)
    logging.info('CRIOU INSTANCIA DO CRAWLER')
    crawler.run()
