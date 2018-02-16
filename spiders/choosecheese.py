import re

from urllib.parse import parse_qs, urlencode, urlparse
from . import ShopSpider

class ChooseCheeseSpider(ShopSpider):
    name = 'choosecheese'
    allowed_domains = ['choosecheese.kr']

    parameters = ['xcode', 'mcode']

    def parse(self, response):
        yield from self.parse_products(response)

        for page in response.css('#mk_pager a'):
            yield response.follow(page, callback=self.parse)

    def parse_products(self, response):
        products = response.css('table.product_table')
        if not products:
            raise ValueError('Failed to find products')

        for product in products:
            if self.extract_with_css(product, 'font[color="red"]::text') == '(품절)':
                continue

            url = response.urljoin(self.extract_with_css(product, 'td.Brand_prodtHeight a::attr(href)'))
            query = parse_qs(urlparse(url).query)

            customer_price = self.extract_with_css(product, 'font.brandconprice span::text')
            if not customer_price:
                continue
            customer_price = int(re.sub(r'[^\d]', '', customer_price))

            current_price = self.extract_with_css(product, 'span.brandprice span::text')
            if not current_price:
                continue
            current_price = int(re.sub(r'[^\d]', '', current_price))

            yield {
                'url': url,
                'id': query.get('branduid', [None])[0],
                'image_url': response.urljoin(self.extract_with_css(product, 'td.Brand_prodtHeight img::attr(src)')),
                'name': self.extract_with_css(product, 'a font.brandbrandname::text'),
                'price': current_price,
                'discount_rate': (customer_price - current_price) / customer_price,
            }

    def url_of(self, xcode, mcode):
        return '{list_url}?{query}'.format(
            list_url='http://choosecheese.kr/shop/shopbrand.html',
            query=urlencode({
                'xcode': xcode,
                'mcode': mcode,
                'type': 'X',
            })
        )