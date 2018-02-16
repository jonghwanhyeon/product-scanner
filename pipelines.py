import logging
import os
import pickle
import re

import requests
import scrapy

import config
import notification

from functools import partial

os.makedirs('seen/', exist_ok=True)
seen_filename_template = os.path.join(
    'seen',
    '{name}.pickle'
)

without_whitespace = partial(re.sub, r'\s', '')

class SearchKeywordPipeline:
    def __init__(self):
        self.logger = logging.getLogger('searchkeywordpipeline')
        self.logger.setLevel(logging.INFO)

        self.keywords = [
            (without_whitespace(item), item) if isinstance(item, str)
            else (without_whitespace(item[0]), item[1])
            for item in config.keywords
        ]

        self.crawled = set()
        self.seen = set()

    def open_spider(self, spider):
        seen_filename = seen_filename_template.format(name=spider.name)

        if os.path.exists(seen_filename):
            with open(seen_filename, 'rb') as input_file:
                self.seen = pickle.load(input_file)

    def close_spider(self, spider):
        seen_filename = seen_filename_template.format(name=spider.name)

        with open(seen_filename, 'wb') as output_file:
            pickle.dump(self.crawled, output_file)

    def process_item(self, item, spider):
        if item['id'] in self.crawled:
            raise scrapy.exceptions.DropItem('Duplicated item: {id}'.format(id=item['id']))

        self.crawled.add(item['id'])

        for keyword_without_space, keyword in self.keywords:
            if keyword_without_space in without_whitespace(item['name']):
                if item['id'] not in self.seen:
                    self.logger.info('Product found: {name} ({keyword})'.format(
                        name=item['name'],
                        keyword=keyword_without_space
                    ))
                    self.notify(item, keyword)
                    break

        return item

    def notify(self, item, keyword):
        title = '{keyword} - ₩{price:,} (-{discount_rate:.0f}%)'.format(
            keyword=keyword,
            price=item['price'],
            discount_rate=item['discount_rate'] * 100
        )

        parameters = {
            'title': '{keyword} - ₩{price:,} (-{discount_rate:.0f}%)'.format(
                keyword=keyword,
                price=item['price'],
                discount_rate=item['discount_rate'] * 100
            ),
            'message': item['name'],
            'url': item['url'],
        }

        response = requests.get(item['image_url'])
        if response.status_code == 200:
            parameters['attachment'] = response.content

        notification.send(**config.pushover, **parameters)
        self.logger.info('Notification sent: {message}'.format(message=item['name']))
