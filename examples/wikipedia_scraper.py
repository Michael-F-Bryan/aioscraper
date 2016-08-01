import logging
from urllib.parse import urljoin
from aioscraper import BaseCrawler, Job


class MyCrawler(BaseCrawler):
    initial_urls = ['http://en.wikipedia.org/']

    def handle_initial(self, page, job):
        for link in page.soup.find_all('a'):
            try:
                href = link['href']
            except KeyError as e:
                continue

            if href.startswith('/'):
                href = urljoin('http://en.wikipedia.org/', href)

            # Only get pages which are on the "en.wikipedia.org" domain
            if 'wikipedia.org' in href:
                new_job = Job('page', url=href)
                yield new_job

    def handle_page(self, page, job):
        print(page)


config = {
        'log-level': logging.INFO,
        }
bot = MyCrawler(config)
bot.run()

