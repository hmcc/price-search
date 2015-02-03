""" Scrapy project settings.

For more information, see http://doc.scrapy.org/en/latest/topics/settings.html
"""

BOT_NAME = 'pricesearch'

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'pricesearch (+http://www.yourdomain.com)'

# Feed export - JSON lines to file
FEED_URI = 'home/heather/scrape.json'
FEED_FORMAT = 'jsonlines'
