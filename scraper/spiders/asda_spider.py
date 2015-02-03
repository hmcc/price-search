"""
This module contains a spider for groceries.asda.com.
"""

import collections
import json
from urlparse import urljoin

from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders.crawl import Rule, CrawlSpider
from scrapy.http.request import Request
from scrapy.http.response.html import HtmlResponse
from scrapy.http.response.text import TextResponse
from scrapy.spider import Spider
from scrapy.utils.response import get_base_url

from scraper.items import SupermarketItem
class AsdaSpider(Spider):

    """
    This class is a subclass of scrapy.Spider that scrapes the Asda site.
    """
    name = "asda"
    base_url = "http://groceries.asda.com"
    start_urls = [
        urljoin(base_url, "api/categories/viewmenu")
    ]

    def get_title(self, cell):
        """Extract the title from an item"""

        return cell.css("span.title::text").extract()

    def get_price(self, cell):
        """Extract the price from a list item"""

        return cell.css("span.price::text").extract()

    def get_unit_price(self, cell):
        """Extract the unit price (e.g. price per 100g) from a list item"""

        return cell.css("span.priceInformation::text").extract()

    def _extract_links(self, obj):
        if 'categories' in obj:
            return self._extract_links(obj['categories'])
        if 'type' in obj and obj['type'] == 'shelf' and 'id' in obj:
            return ['asda-webstore/landing/home.shtml#/shelf/%s/1/so_false' % obj['id']]
        if isinstance(obj, list):
            links = []
            for o in obj:
                links = links + self._extract_links(o)
            return links


    def parse(self, response):
        """Parse the HTTP response to yield SupermarketItem, and/or
        Requests for more pages.

        Keyword arguments:
        response -- the HTTP response
        """ 
        if isinstance(response, HtmlResponse):
            for cell in response.css("div.product-content"):
                item = SupermarketItem()
                item['title'] = self.get_title(cell)
                item['price'] = self.get_price_pence(cell)
                item['unit_price'] = self.get_unit_price(cell)
                yield item
            
        elif isinstance(response, TextResponse):
            json_response = json.loads(response.body_as_unicode())
            for link in self._extract_links(json_response):
                full_link = urljoin(self.base_url, link)
                request = Request(full_link)
                yield request
        
