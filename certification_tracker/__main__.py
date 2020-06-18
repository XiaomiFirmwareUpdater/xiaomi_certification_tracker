"""Xiaomi Certification Tracker entry point"""
from certification_tracker.runner import crawl, reactor

if __name__ == '__main__':
    crawl()
    reactor.run()
