"""
This module contains subclasses of scrapy.Item.

For more information, see http://doc.scrapy.org/en/latest/topics/items.html
"""
import scrapy


class MySupermarketItem(scrapy.Item):
    """
    This class represents a single item for sale on mysupermarket.co.uk
    Title and price should be self-explanatory; the unit price is the price
    per 100g/100ml/item, and the subtitle is used by mysupermarket.co.uk
    to distinguish between similar items e.g. "Yorkshire Tea (160)" and
    "Yorkshire Tea (80)" where "Yorkshire Tea" is the title and (160)" or 
    "(80)" is the subtitle.
    """
    title = scrapy.Field()
    subtitle = scrapy.Field()
    price = scrapy.Field()
    unit_price = scrapy.Field()
