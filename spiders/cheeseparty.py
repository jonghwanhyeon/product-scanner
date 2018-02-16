import re

from urllib.parse import parse_qs, urlencode, urlparse
from . import ShopSpider

class CheesePartySpider(ShopSpider):
    name = 'cheeseparty'
    allowed_domains = ['cheeseparty.co.kr']

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

            url = response.urljoin(self.extract_with_css(product, 'p.name a::attr(href)'))
            query = urlparse(url).query

            records = product.css('ul.xans-product > li')
            if len(records) <= 3: # not on sale
                continue

            prices = []
            for text in product.css('ul.xans-product > li span::text').extract():
                if re.search(r'[\d\,]+원', text):
                    prices.append(int(re.sub(r'[^\d]', '', text)))

            if (not prices) or (len(prices) != 2):
                continue

            customer_price, current_price = prices

            yield {
                'url': url,
                'id': parse_qs(query).get('product_no', [None])[0],
                'image_url': response.urljoin(self.extract_with_css(product, 'img.thumb::attr(src)')),
                'name': self.extract_with_css(product, 'p.name a > span::text'),
                'price': current_price,
                'discount_rate': (customer_price - current_price) / customer_price,
            }

    def url_of(self, cate_no):
        return '{list_url}?{query}'.format(
            list_url='http://cheeseparty.co.kr/product/list.html',
            query=urlencode({
                'cate_no': cate_no,
            })
        )