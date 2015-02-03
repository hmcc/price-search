"""
This module contains convenience methods for working with the application
config.
"""
from ConfigParser import ConfigParser


cfg = ConfigParser()
cfg.read("app.cfg")

supermarket_spiders = dict(cfg.items('spiders'))


def supermarket_names():
    return supermarket_spiders.keys()


def supermarket_spider(supermarket):
    return supermarket_spiders[supermarket]
