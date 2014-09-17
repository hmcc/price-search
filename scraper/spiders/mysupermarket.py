"""
This module contains subclasses of scrapy.Spider used for scraping 
mysupermarket.co.uk.
"""

from scrapy import Request, Spider

from ..items import MySupermarketItem


class MySupermarketSpider(Spider):
    """
    This class is a subclass of scrapy.Spider that scrapes the "Savvy Buys"
    pages of mysupermarket.co.uk for a single supermarket.
    """
    name = "mysupermarket"
    allowed_domains = ["mysupermarket.co.uk"]

    def __init__(self, url):
        """
        Set up the spider to start scraping from the given URL. URLs should
        be the first page of "Savvy Buys" for a supermarket and should be
        read from the app.cfg file.
        
        For multiple supermarkets, use multiple spiders.
        
        Keyword arguments:
        url -- a single URL to start from.
        """
        Spider.__init__(self)
        self.start_urls = [url]

    def get_title(self, cell):
        """Extract the title from a list item"""

        # Titles have a trailing space
        return cell.css("span.ProductName::text").extract()[0][:-1]

    def get_subtitle(self, cell):
        """Extract the subtitle from a list item"""

        subtitle_elements = cell.css("span.NameSuffix::text").extract()
        # Not all items have a subtitle
        if subtitle_elements:
            return subtitle_elements[0]

    def get_price(self, cell):
        """Extract the price from a list item"""

        price_container = cell.css("span.Price")
        offer_price_element = price_container.css(".Offer::text").extract()
        if offer_price_element:
            # Offer elements can be either [" any", " 2 for 50p"] or [" 50p"]
            # Take the last in the list then strip leading space
            return offer_price_element[-1][1:]
        else:
            return price_container.css("span.priceClass::text").extract()[0]

    def get_unit_price(self, cell):
        """Extract the unit price (e.g. price per 100g) from a list item"""

        ppu_elements = cell.css("span.PPU > ::text").extract()
        # 5 children with both old and new unit price
        # e.g. (50p/40p/100g) as ["(", "50p/", "40p/", "100g", ")"]
        if len(ppu_elements) == 5:
            return "".join(ppu_elements[2:4])

        # 1 child with new price surrounded by 2 text sections
        # e.g. (50p/100g) as text ["(", "100g)"] and children ["50p/"]
        elif len(ppu_elements) == 1:
            return ppu_elements[0] + cell.css("span.PPU::text").extract()[1][:-1]

    def parse(self, response):
        """Parse the HTTP response to yield MySupermarketItem, and/or
        Requests for more pages.

        Keyword arguments:
        response -- the HTTP response
        """
        for cell in response.css("li.MspProductListCell"):
            item = MySupermarketItem()
            item['title'] = self.get_title(cell)
            item['subtitle'] = self.get_subtitle(cell)
            item['price'] = self.get_price(cell)
            item['unit_price'] = self.get_unit_price(cell)
            yield item

        next_page = response.css(
            "a.NextPage:not(.Disabled)::attr(href)").extract()
        if next_page:
            yield Request(next_page[0], callback=self.parse)
