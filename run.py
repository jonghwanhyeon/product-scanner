import inspect
import logging
import os

from importlib import import_module

from scrapy.crawler import CrawlerProcess

from productscanner import base_path, config

def load_spiders():
    for name in config.spiders:
        module = import_module('productscanner.spiders.{name}'.format(name=name))
        for _, member in inspect.getmembers(module, inspect.isclass):
            if member.__module__ != module.__name__:
                continue

            if member.name == name:
                yield member

def main():
    logs_directory = os.path.join(base_path, 'logs')
    os.makedirs(logs_directory, exist_ok=True)

    handler = logging.handlers.TimedRotatingFileHandler(
        os.path.join(logs_directory, 'product-scanner.log'),
        when='midnight',
        backupCount=7,
        encoding='utf-8'
    )
    handler.setFormatter(logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s'))
    handler.setLevel(logging.DEBUG)
    # handler.setLevel(logging.INFO)
    logging.getLogger().addHandler(handler)

    process = CrawlerProcess({
        'USER_AGENT': config.crawler['user_agent'],
        'ITEM_PIPELINES': {
            'productscanner.pipelines.SearchKeywordPipeline': 500,
        },
        'EXTENSIONS': {
            'productscanner.extensions.NotifyExceptionExtension': 500,
        }
    }, install_root_handler=False)

    for spider in load_spiders():
        for parameter in config.spiders.get(spider.name, []):
            process.crawl(spider, **parameter)

    process.start()

if __name__ == '__main__':
    main()