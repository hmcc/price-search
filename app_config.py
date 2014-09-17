"""
This module contains convenience methods for working with the application
config.
"""
from ConfigParser import ConfigParser
from os.path import join, dirname, realpath


cfg = ConfigParser()
cfg.read("app.cfg")

supermarket_urls = dict(cfg.items('urls'))

supermarket_files = {}
working_dir = dirname(realpath(__file__))
for k, v in cfg.items('filenames'):
    supermarket_files[k] = join(working_dir, v)


def supermarket_names():
    return supermarket_files.keys()


def supermarket_filename(supermarket):
    return supermarket_files[supermarket]


def supermarket_filenames():
    return supermarket_files.values()


def supermarket_url(supermarket):
    return supermarket_urls[supermarket]
