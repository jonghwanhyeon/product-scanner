import logging
import os


from scrapy.crawler import CrawlerProcess
from spiders import ImbakSpider, ThirtyMallSpider, CheeseQueenSpider, CheesePartySpider, ChooseCheeseSpider

os.makedirs('logs/', exist_ok=True)
handler = logging.handlers.TimedRotatingFileHandler(
    'logs/product-scanner.log',
    when='midnight',
    backupCount=7,
    encoding='utf-8'
)
handler.setFormatter(logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s'))
# handler.setLevel(logging.DEBUG)
handler.setLevel(logging.INFO)
logging.getLogger().addHandler(handler)

process = CrawlerProcess({
    'USER_AGENT': config.crawler['user_agent'],
    'ITEM_PIPELINES': {
        'pipelines.SearchKeywordPipeline': 500,
    },
    'EXTENSIONS': {
        'extensions.NotifyExceptionExtension': 500,
    }
}, install_root_handler=False)

spiders = [ImbakSpider, ThirtyMallSpider, CheeseQueenSpider, CheesePartySpider, ChooseCheeseSpider]
for spider in spiders:
    for parameter in config.spiders.get(spider.name, []):
        process.crawl(spider, **parameter)

process.start()from productscanner import base_path, config
