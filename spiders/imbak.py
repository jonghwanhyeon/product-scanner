import re

from urllib.parse import parse_qs, urlencode, urlparse
from . import ShopSpider

class ImbakSpider(ShopSpider):
    name = 'imbak'
    allowed_domains = ['imbak.co.kr']

    parameters = ['category']

    def parse(self, response):
        products = response.css('div.cate_item li')
        if not products:
            raise ValueError('Failed to find products')

        for product in products:
            url = response.urljoin(self.extract_with_css(product, 'a::attr(href)'))
            query = urlparse(url).query

            customer_price = self.extract_with_css(product, 'span.customer_price::text')
            if not customer_price:
                continue
            customer_price = int(re.sub(r'[^\d]', '', customer_price))

            current_price = self.extract_with_css(product, 'span.real_price::text')
            if not current_price:
                continue
            current_price = int(re.sub(r'[^\d]', '', current_price))

            yield {
                'url': url,
                'id': parse_qs(query).get('goodsno', [None])[0],
                'image_url': response.urljoin(self.extract_with_css(product, 'img.cate_img::attr(src)')),
                'name': self.extract_with_css(product, 'p.goods_nm::text'),
                'price': current_price,
                'discount_rate': (customer_price - current_price) / customer_price,
            }

    def url_of(self, category):
        return '{list_url}?{query}'.format(
            list_url='http://www.imbak.co.kr/shop/goods/goods_list.php',
            query=urlencode({ 'category': category })
        )
