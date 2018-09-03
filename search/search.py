"""
This module contains functions for searching the data scraped from 
mysupermarket.co.uk using pricesearch.scraper.
"""
from json import loads
import logging


logger = logging.getLogger('price_search')


def search_file(search_phrases, filename, match_fn=lambda item: output_match(item)):
    """Search the given JSON file for the given phrases, calling match_fn
    each time a match is found
        
    Keyword arguments:
    search_phrases -- a list of lists of words to search
    filename -- the full path to the scraped JSON data
    match_fn -- function to call if a match is found
    """
    with open(filename) as f:
        content = f.readlines()

    for line in content:
        item = loads(line)
        for phrase in search_phrases:
            match = len(phrase)
            for word in phrase:
                match = match and 'title' in item and word.lower() in item[
                    'title'].lower()
            if match:
                match_fn(item)


def output_match(item):
    """Print the item.
    
    Keyword arguments:
    item -- the item to print
    """
    logger.info("%s %s %s %s" %
                (item['title'], item['subtitle'], item['price'], item['unit_price']))
