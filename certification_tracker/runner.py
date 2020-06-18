from scrapy import spiderloader
from scrapy.crawler import CrawlerRunner
from scrapy.utils import project
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

configure_logging()


@inlineCallbacks
def crawl():
    settings = project.get_project_settings()
    spider_loader = spiderloader.SpiderLoader.from_settings(settings)
    spiders = spider_loader.list()
    classes = [spider_loader.load(name) for name in spiders]
    for my_spider in classes:
        runner = CrawlerRunner(settings)
        yield runner.crawl(my_spider)
    reactor.stop()
