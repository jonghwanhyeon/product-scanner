import logging
import scrapy

from . import notification

class NotifyExceptionExtension:
    def __init__(self):
        self.logger = logging.getLogger('notifyexceptionextension')
        self.logger.setLevel(logging.INFO)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        instance = cls(*args, **kwargs)
        crawler.signals.connect(instance.spider_error, signal=scrapy.signals.spider_error)

        return instance

    def spider_error(self, failure, response, spider):
        notification.send(
            title='[{name}] An error occurred'.format(name=spider.name.upper()),
            message=failure.getErrorMessage(),
        )
        self.logger.info('Notification sent: {message}'.format(message=parameters['title']))