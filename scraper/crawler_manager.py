"""
This module contains a single class that manages the scraping of data
from one or more supermarkets on mysupermarket.co.uk
"""
import inspect
from os import path
import pkgutil

from scrapy import signals
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings

from app_config import supermarket_names, supermarket_spider

from .reactor_control import ReactorControl


class CrawlerManager():

    """
    A "crawler manager" that manages scraping the supermarket websites. 
    For each supermarket, it creates and starts a crawler.
    """

    def __init__(self, supermarkets=supermarket_names()):
        """Create a CrawlerManager for the given supermarket(s).

        Keyword arguments:
        supermarkets -- a list of supermarkets to scrape
        """
        self.supermarkets = supermarkets
        self.reactor_control = ReactorControl()
        self.spiders = self.get_spiders()

    def get_spiders(self):
        current_module_path = path.basename(path.dirname(__file__))
        spider_module_path = path.join(current_module_path, "spiders")
        spider_modules = pkgutil.iter_modules(path=[spider_module_path])
        spiders = {}

        for loader, mod_name, ispkg in spider_modules:
            loaded_module = loader.find_module(mod_name).load_module(mod_name)
            for name, obj in inspect.getmembers(loaded_module):
                spiders[name] = obj

        return spiders

    def setup_crawler(self, supermarket, reactor_control):
        """Set up the Scrapy crawler. 
        See http://doc.scrapy.org/en/latest/topics/practices.html#run-scrapy-from-a-script.

        Keyword arguments:
        supermarket -- the supermarket whose crawler should be set up
        """

        settings = get_project_settings()

        spider_name = supermarket_spider(supermarket)
        spider = self.spiders[spider_name]()

        crawler = Crawler(settings)
        crawler.signals.connect(
            reactor_control.remove_crawler, signal=signals.spider_closed)
        crawler.configure()
        crawler.crawl(spider)
        crawler.start()
        reactor_control.add_crawler()

    def get_data(self):
        if self.supermarkets:
            reactor_control = ReactorControl()
            for supermarket in self.supermarkets:
                self.setup_crawler(supermarket, reactor_control)

            reactor_control.start_crawling()
