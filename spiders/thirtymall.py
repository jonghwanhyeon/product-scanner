import re

from urllib.parse import parse_qs, urlencode, urlparse
from . import ShopSpider

class ThirtyMallSpider(ShopSpider):
    name = 'thirtymall'
    allowed_domains = ['thirtymall.com']

    parameters = ['code']

    def parse(self, response):
        yield from self.parse_products(response)

        for page in response.css('ul.pagination li:not(.active) a'):
            yield response.follow(page, callback=self.parse)

    def parse_products(self, response):
        products = response.css('div.bestPro.Pros')
        if not products:
            raise ValueError('Failed to find products')

        for product in products:
            url = response.urljoin(self.extract_with_css(product, 'p.proTitle a::attr(href)'))
            query = parse_qs(urlparse(url).query)

            price = self.extract_with_css(product, 'div.proPrice span.price02::text')
            if not price:
                continue
            price = int(re.sub(r'[^\d]', '', price))

            discount_rate = self.extract_with_css(product, 'div.proPrice span.price03::text')
            if not discount_rate:
                continue
            discount_rate = int(re.sub(r'[^\d]', '', discount_rate)) / 100

            yield {
                'url': url,
                'id': query.get('no', [None])[0],
                'image_url': response.urljoin(self.extract_with_css(product, 'span.goodsDisplayImageWrap img::attr(src)')),
                'name': self.extract_with_css(product, 'p.proTitle a::text'),
                'price': price,
                'discount_rate': discount_rate,
            }

    def url_of(self, code):
        return '{list_url}?{query}'.format(
            list_url='http://www.thirtymall.com/goods/catalog',
            query=urlencode({
                'code': code,
                'perpage': 100,
            })
        )