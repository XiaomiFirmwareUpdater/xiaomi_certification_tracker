from scrapy import spiderloader
from scrapy.crawler import CrawlerRunner
from scrapy.utils import project
from scrapy.utils.log import configure_logging
from twisted.internet import reactor

configure_logging()


def run():
    settings = project.get_project_settings()
    spider_loader = spiderloader.SpiderLoader.from_settings(settings)
    spiders = spider_loader.list()
    classes = [spider_loader.load(name) for name in spiders]
    runner = CrawlerRunner()
    for spider in classes:
        runner.crawl(spider)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
