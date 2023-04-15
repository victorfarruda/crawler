from unittest import TestCase
from unittest.mock import patch, Mock

from selenium import webdriver

from src.crawler import CrawlerFinanceYahoo


class TestCrawler(TestCase):
    def setUp(self) -> None:
        self.crawler = CrawlerFinanceYahoo(region='Brazil')
        self.crawler.driver = Mock()

    def test_can_create_object(self):
        self.assertIsInstance(self.crawler, CrawlerFinanceYahoo)

    def test_get_options(self):
        options = self.crawler.get_options()
        self.assertIsInstance(options, webdriver.ChromeOptions)

    def test_get_driver(self):
        driver = self.crawler.get_driver()
        self.assertIsInstance(driver, webdriver.Chrome)

    def test_login(self):
        self.crawler.login()
        self.crawler.driver.find_element.assert_called()

    def test_click_element(self):
        self.crawler.click_element('element')
        self.crawler.driver.find_element.assert_called()

    def test_process_tbody(self):
        tbody = [
            [Mock(text='Testesymbol'), Mock(text='Testename'), Mock(text='Testeprice'), Mock(text='Teste')],
            [Mock(text='Teste2symbol'), Mock(text='Teste2name'), Mock(text='Teste2price'), Mock(text='Teste2')],
        ]
        result = self.crawler.process_tbody(tbody)
        self.assertEqual(result, [
            {'symbol': 'Testesymbol', 'name': 'Testename', 'price(intraday)': 'Testeprice'},
            {'symbol': 'Teste2symbol', 'name': 'Teste2name', 'price(intraday)': 'Teste2price'}
        ])

    def test_create_csv(self):
        with patch('src.crawler.open') as open_mock:
            self.crawler.create_json([
                {'symbol': 'Testesymbol', 'name': 'Testename', 'price(intraday)': 'Testeprice'},
                {'symbol': 'Teste2symbol', 'name': 'Teste2name', 'price(intraday)': 'Teste2price'}
            ])
            open_mock.assert_called_once()

    def test_create_json(self):
        with patch('src.crawler.open') as open_mock:
            with patch('json.dumps') as json_mock:
                self.crawler.create_json([
                    {'symbol': 'Testesymbol', 'name': 'Testename', 'price(intraday)': 'Testeprice'},
                    {'symbol': 'Teste2symbol', 'name': 'Teste2name', 'price(intraday)': 'Teste2price'}
                ])
                open_mock.assert_called_once()
                json_mock.assert_called_once()

    @patch('src.crawler.BeautifulSoup', Mock())
    def test_process_table(self):
        self.crawler.process_tbody = Mock()
        self.crawler.create_csv = Mock()
        self.crawler.create_json = Mock()

        self.crawler.process_table()

        self.crawler.driver.find_element.assert_called()
        self.crawler.process_tbody.assert_called_once()
        self.crawler.create_csv.assert_called_once()
        self.crawler.create_json.assert_called_once()
        self.crawler.driver.close.assert_called_once()

    def test_load_page(self):
        driver = self.crawler.get_driver

        self.crawler.get_driver = Mock()

        self.crawler.load_page()
        self.crawler.driver.get.assert_called_once()

        self.crawler.get_driver = driver

    def test_select_new_region(self):
        self.crawler.select_new_region()
        self.crawler.driver.find_element.assert_called()
        self.crawler.driver.execute_script.assert_called()

    def test_run(self):
        self.crawler.load_page = Mock()
        self.crawler.login = Mock()
        self.crawler.click_element = Mock()
        self.crawler.select_new_region = Mock()
        self.crawler.process_table = Mock()

        self.crawler.run()

        self.crawler.click_element.assert_called()
        self.crawler.load_page.assert_called_once()
        self.crawler.login.assert_called_once()
        self.crawler.select_new_region.assert_called_once()
        self.crawler.process_table.assert_called_once()
