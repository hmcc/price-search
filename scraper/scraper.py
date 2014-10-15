"""
This module contains a single class that manages the scraping of data
from one or more supermarkets on mysupermarket.co.uk
"""
from datetime import datetime
from os import remove
from os.path import isfile, getmtime
from time import time

from scrapy import signals
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings

from app_config import supermarket_names, supermarket_url, supermarket_filename

from .reactor_control import ReactorControl
from .spiders.mysupermarket import MySupermarketSpider


class CachingScraper():
    """
    A "crawler manager" that manages scraping mysupermarket.co.uk for one or 
    more supermarkets. For each supermarket, it checks the cache file then 
    creates and starts a crawler if appropriate.
    """

    def __init__(self, supermarkets=supermarket_names(), force_refresh=False):
        """Create a CachingScraper for the given supermarket(s).
        
        Keyword arguments:
        supermarkets -- a list of supermarkets to scrape
        force_refresh -- if True, cachefiles will not be used
        """
        self.force_refresh = force_refresh
        self.supermarkets = supermarkets
        self.reactor_control = ReactorControl()

    def cache_exists(self, supermarket):
        """Check whether a JSON file already exists for data scraped from
        the given supermarket, and if so, whether it was created today.
        Note that 'created today' is not the same as 'age < 24 hours'. Prices
        are assumed to change overnight so a cachefile created at 9pm
        yesterday is considered out of date at 9am today (but a cachefile
        created at 9am is not out of date at 9pm).

        Keyword arguments:
        supermarket -- the supermarket whose cachefile should be checked
        """
        cachefile = supermarket_filename(supermarket)
        if not isfile(cachefile):
            return False

        mtime = datetime.fromtimestamp(getmtime(cachefile))
        now = datetime.fromtimestamp(time())
        return mtime.day == now.day

    def setup_crawler(self, supermarket, reactor_control):
        """Set up the Scrapy crawler. 
        See http://doc.scrapy.org/en/latest/topics/practices.html#run-scrapy-from-a-script.
        
        Keyword arguments:
        supermarket -- the supermarket whose crawler should be set up
        """
        
        cachefile = supermarket_filename(supermarket)
        if isfile(cachefile):
            remove(cachefile)
            
        settings = get_project_settings()

        url = supermarket_url(supermarket)
        settings.set('FEED_URI', supermarket_filename(supermarket))

        spider = MySupermarketSpider(url)
        crawler = Crawler(settings)
        crawler.signals.connect(reactor_control.remove_crawler, signal=signals.spider_closed)
        crawler.configure()
        crawler.crawl(spider)
        crawler.start()
        reactor_control.add_crawler()

    def get_data(self):
        """Main entry point for the scraper class. Crawl or get data from cache
        for the configured supermarkets. Supermarkets are set in __init__.
        """
        if self.force_refresh:
            supermarkets_to_crawl = self.supermarkets
        else:
            supermarkets_to_crawl = [x for x in self.supermarkets if not self.cache_exists(x)]
        
        if supermarkets_to_crawl:
            reactor_control = ReactorControl()
            for supermarket in supermarkets_to_crawl:
                self.setup_crawler(supermarket, reactor_control)

            reactor_control.start_crawling()
