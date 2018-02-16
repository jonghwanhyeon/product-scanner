import logging
import scrapy

class ShopSpider(scrapy.Spider):
    name = None
    allowed_domains = []

    parameters = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger.setLevel(logging.INFO)

    def start_requests(self):
        arguments = {}
        for name in self.parameters:
            arguments[name] = getattr(self, name, None)
            if arguments[name] is None:
                raise ValueError('no `{name}`'.format(name=name))

        url = self.url_of(**arguments)

        self.logger.info('Starting request: {url}'.format(url=url))
        yield scrapy.Request(url, self.parse)

    def url_of(self, parameters):
        raise NotImplementedError()

    def extract_with_css(self, element, selector):
        text = element.css(selector).extract_first()
        return text.strip() if text else None

    def extract_with_xpath(self, element, path):
        text = element.xpath(path).extract_first()
        return text.strip() if text else None

from .imbak import ImbakSpider
from .thirtymall import ThirtyMallSpider
from .cheesequeen import CheeseQueenSpider
from .cheeseparty import CheesePartySpider
from .choosecheese import ChooseCheeseSpider