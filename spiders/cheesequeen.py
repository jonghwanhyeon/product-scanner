import re

from urllib.parse import parse_qs, urlencode, urlparse
from . import ShopSpider

class CheeseQueenSpider(ShopSpider):
    name = 'cheesequeen'
    allowed_domains = ['cheesequeen.co.kr']

    parameters = ['code']

    def parse(self, response):
        yield from self.parse_products(response)

        for page in response.css('div.paging_navigation a:not(.on)'):
            yield response.follow(page, callback=self.parse)

    def parse_products(self, response):
        products = response.css('table.goodsDisplayItemWrap')
        if not products:
            raise ValueError('Failed to find products')

        for product in products:
            rows = product.css('tr')
            if rows[11].css('img'): # out of stock
                continue

            url = response.urljoin(self.extract_with_css(product, 'a::attr(href)'))
            query = parse_qs(urlparse(url).query)

            customer_price = self.extract_with_css(rows[6], 'span::text')
            if not customer_price:
                continue
            customer_price = int(re.sub(r'[^\d]', '', customer_price))

            current_price = self.extract_with_css(rows[8], 'span::text')
            if not current_price:
                continue
            current_price = int(re.sub(r'[^\d]', '', current_price))

            yield {
                'url': url,
                'id': query.get('no', [None])[0],
                'image_url': response.urljoin(self.extract_with_css(product, 'span.goodsDisplayImageWrap img::attr(src)')),
                'name': self.extract_with_css(rows[2], 'span::text'),
                'price': current_price,
                'discount_rate': current_price / customer_price,
            }

    def url_of(self, code):
        return '{list_url}?{query}'.format(
            list_url='http://cheesequeen.co.kr/goods/catalog',
            query=urlencode({
                'code': code,
                'perpage': 200,
            })
        )