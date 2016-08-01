==========
Aioscraper
==========

A web scraper building on the new asyncio library and designed to be super easy
for people to use.

Installation
============

From Source
-----------

First you need to get the code from Github::

    git clone https://github.com/Michael-F-Bryan/aioscraper.git

Then run the `setup.py` module::

    python setup.py install


Example
=======

Using the scraper is fairly simple, you just need to subclass the BaseCrawler,
writing your own implementations for each task handler.

::

    from aioscraper import BaseCrawler, Job

    class MyCrawler(BaseCrawler):
        initial_urls = ['http://google.com/']

        def handle_initial(self, page, job):
            """
            A handler to deal with the initial urls and queue more jobs to be run
            by the crawler.
            """
            print(job)

            for link in page.soup.find_all('a'):
                href = link['href']
                print('found a link:', href)

                # Make sure we have an absolute url
                if href.startswith('/'):
                    href = 'http://google.com' + href

                yield Job('page', url=href)

        def handle_page(self, page, job):
            """
            Write a handler to deal with the "page" jobs.
            """
            print(page, job)


    if __name__ == '__main__':
        bot = MyCrawler()
        bot.run()
