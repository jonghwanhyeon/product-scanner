import logging
import scrapy

from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

class ShopSpider(scrapy.Spider):
    name = None
    allowed_domains = []

    start_url = None
    parameters = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger.setLevel(logging.INFO)

    def start_requests(self):
        parameters = self.load_parameters()
        url = self.start_url_of(parameters)

        self.logger.info('Starting request: {url}'.format(url=url))
        yield scrapy.Request(url, self.parse)

    def load_parameters(self):
        arguments = {}
        for name in self.parameters:
            value = getattr(self, name, None)
            if value is None:
                raise ValueError('no `{name}`'.format(name=name))

            arguments[name] = value

        return arguments

    def start_url_of(self, parameters):
        components = list(urlparse(self.start_url))
        query = parse_qs(components[4]) # 4: query

        merged_query = dict(query, **parameters)
        components[4] = urlencode(merged_query, doseq=True) # 4: query

        return urlunparse(components)

from .imbak import ImbakSpider
from .thirtymall import ThirtyMallSpider
from .cheesequeen import CheeseQueenSpider
from .cheeseparty import CheesePartySpider
from .choosecheese import ChooseCheeseSpider