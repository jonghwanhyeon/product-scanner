import re

from urllib.parse import parse_qs, urlparse

from . import ShopSpider
from utils import extract_with_css, only_digit

class ImbakSpider(ShopSpider):
    name = 'imbak'
    allowed_domains = ['imbak.co.kr']

    start_url = 'http://www.imbak.co.kr/shop/goods/goods_list.php'
    parameters = ['category']

    def parse(self, response):
        yield from self.parse_products(response)
        
    def parse_products(self, response):
        products = response.css('div.cate_item li')
        if not products:
            raise ValueError('Failed to find products')

        for product in products:
            url = response.urljoin(extract_with_css(product, 'a::attr(href)'))
            query = urlparse(url).query

            customer_price = extract_with_css(product, 'span.customer_price::text')
            if not customer_price:
                continue
            customer_price = int(only_digit(customer_price))

            current_price = extract_with_css(product, 'span.real_price::text')
            if not current_price:
                continue
            current_price = int(only_digit(current_price))

            yield {
                'url': url,
                'id': parse_qs(query).get('goodsno', [None])[0],
                'image_url': response.urljoin(extract_with_css(product, 'img.cate_img::attr(src)')),
                'name': extract_with_css(product, 'p.goods_nm::text'),
                'price': current_price,
                'discount_rate': (customer_price - current_price) / customer_price,
            }
