import re

from urllib.parse import parse_qs, urlparse

from . import ShopSpider
from ..utils import extract_with_css, only_digit

class CheesePartySpider(ShopSpider):
    name = 'cheeseparty'
    allowed_domains = ['cheeseparty.co.kr']

    start_url = 'http://cheeseparty.co.kr/product/list.html'
    parameters = ['cate_no']

    def parse(self, response):
        yield from self.parse_products(response)

        paging = response.css('div.df-base-paging')
        next_page = paging.xpath('.//img[@alt="next"]/..')[0]

        if next_page.xpath('@href').extract_first().strip() != '#none':
            yield response.follow(next_page, callback=self.parse)

    def parse_products(self, response):
        products = response.css('ul.prdList > li')
        if not products:
            raise ValueError('Failed to find products')

        for product in products:
            if product.css('div.icon img[alt="품절"]'):
                continue

            url = response.urljoin(extract_with_css(product, 'p.name a::attr(href)'))
            query = urlparse(url).query

            records = product.css('ul.xans-product > li')
            if len(records) <= 3: # not on sale
                continue

            prices = []
            for text in product.css('ul.xans-product > li span::text').extract():
                if re.search(r'[\d\,]+원', text):
                    prices.append(int(only_digit(text)))

            if (not prices) or (len(prices) != 2):
                continue

            customer_price, current_price = prices

            yield {
                'url': url,
                'id': parse_qs(query).get('product_no', [None])[0],
                'image_url': response.urljoin(extract_with_css(product, 'img.thumb::attr(src)')),
                'name': extract_with_css(product, 'p.name a > span::text'),
                'price': current_price,
                'discount_rate': (customer_price - current_price) / customer_price,
            }