"""
This module contains a single class that manages starting and stopping the
Twisted reactor.
"""
from twisted.internet import reactor

class ReactorControl(object):
    """
    A controller for the Twisted reactor which keeps count of the number of
    running crawlers and stops the reactor when there are none left.
    """
    
    def __init__(self):
        """Initialise the counter of running crawlers to 0."""
        self.crawlers_running = 0

    def add_crawler(self):
        """Increment the count of running crawlers."""
        self.crawlers_running += 1

    def remove_crawler(self):
        """Decrement the count of running crawlers, and if there are none left,
        stop the Twisted reactor.
        """
        self.crawlers_running -= 1
        if self.crawlers_running == 0 :
            reactor.stop()
            
    def start_crawling(self):
        reactor.run()