import logging
from urllib.parse import urljoin, urlparse
from aioscraper import BaseCrawler, Job



class Crawler(BaseCrawler):
    initial_urls = ['http://google.com/']

    def prepare(self):
        """
        Do some stuff to set up the crawler. You could set up a database 
        connection or a caching dictionary so you don't retrieve the same 
        page multiple times.
        """
        self.base_url = 'http://google.com/'

    def handle_initial(self, page, job):
        """
        A Crawler that will find all the links on google's home page and
        then fetches the page they point to.
        """
        self.logger.info('Handling an initial job, %r', job)

        for link in page.soup.find_all('a'):
            href = link['href']

            # Make sure the url is absolute
            if href.startswith('/'):
                href = urljoin(self.base_url, href)

            # Anything yielded is assumed to be a Job and the Crawler
            # will queue it to be downloaded.
            yield Job('page', url=href)

    def handle_page(self, page, job):
        """
        We write a handler to deal with any "page" jobs.
        """
        self.logger.info('Page retrieved, %r', page)



if __name__ == "__main__":
    config = {
            'log-level': logging.INFO,
            'max-connections': 20,
            }
    bot = Crawler(config)
    bot.run()
