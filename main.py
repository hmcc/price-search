"""
This module contains the main entry point for the application.
"""
from optparse import OptionParser

from scrapy import log

from app_config import supermarket_names
from scraper.crawler_manager import CrawlerManager
def parse_args():
    """Parse command line arguments."""
    parser = OptionParser()
    parser.add_option("-a", "--all",
                      action='store_true',
                      dest='all',
                      help="search all supermarkets")
    parser.add_option("-s", "--supermarket",
                      action='store',
                      type='string',
                      dest='supermarket',
                      default="asda",
                      help="supermarket to search")

    return parser.parse_args()


def run():
    """Main method.
    Check which supermarkets were requested, create a scraper, then search the 
    scraped data.
    """
    (options, args) = parse_args()
    if (options.all):
        supermarkets = supermarket_names()
    else:
        supermarkets = [options.supermarket]

    scraper = CrawlerManager(supermarkets)
    log.start()
    scraper.get_data()


if __name__ == "__main__":
    run()
