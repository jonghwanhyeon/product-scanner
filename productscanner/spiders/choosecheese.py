import re

from urllib.parse import parse_qs, urlparse

from . import ShopSpider
from ..utils import extract_with_css, only_digit

class ChooseCheeseSpider(ShopSpider):
    name = 'choosecheese'
    allowed_domains = ['choosecheese.kr']

    start_url = 'http://choosecheese.kr/shop/shopbrand.html?type=X'
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
            if extract_with_css(product, 'font[color="red"]::text') == '(품절)':
                continue

            url = response.urljoin(extract_with_css(product, 'td.Brand_prodtHeight a::attr(href)'))
            query = parse_qs(urlparse(url).query)

            customer_price = extract_with_css(product, 'font.brandconprice span::text')
            if not customer_price:
                continue
            customer_price = int(only_digit(customer_price))

            current_price = extract_with_css(product, 'span.brandprice span::text')
            if not current_price:
                continue
            current_price = int(only_digit(current_price))

            yield {
                'url': url,
                'id': query.get('branduid', [None])[0],
                'image_url': response.urljoin(extract_with_css(product, 'td.Brand_prodtHeight img::attr(src)')),
                'name': extract_with_css(product, 'a font.brandbrandname::text'),
                'price': current_price,
                'discount_rate': (customer_price - current_price) / customer_price,
            }