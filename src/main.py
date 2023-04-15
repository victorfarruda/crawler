from decouple import config

from crawler import CrawlerFinanceYahoo

if __name__ == '__main__':
    REGION = config('REGION', 'Brazil')
    crawler = CrawlerFinanceYahoo(region=REGION)
    crawler.run()
