"""
This module contains the main entry point for the application.
"""
import fileinput
from optparse import OptionParser

from scrapy import log

from app_config import supermarket_filename, supermarket_names
from scraper.scraper import CachingScraper
from search.search import search_file


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
    parser.add_option("-r", "--refresh",
                      action='store_true',
                      dest='force_refresh',
                      default=False,
                      help="ignore cache and always fetch fresh data")

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

    scraper = CachingScraper(supermarkets, options.force_refresh)
    log.start()
    scraper.get_data()

    search_phrases = []
    for line in fileinput.input(args):
        search_phrases.append(line.split())

    for supermarket in supermarkets:
        log.msg("*** Savvy buys in %s ***" % supermarket.upper())
        search_file(search_phrases, supermarket_filename(supermarket))


if __name__ == "__main__":
    run()
