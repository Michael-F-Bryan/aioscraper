==========
Quickstart
==========

The scraper works around the central concept of a `Job`. A `Job` is a container
that has a `name` and `url`, and can also hold other information to let the
crawler know how to access a resource (e.g. cookies or extra headers).

When it starts up, the scraper will create an `initial` job for each url in the
scraper's `initial_urls` attribute. It will then queue these jobs to be
handled. When a job is queued, the corresponding web page is fetched
asynchronously and then a handler is run to do something with the fetched web
page. 

Handlers are specified by a method on the Crawler object called `handle_[job
name]` (replacing "[job name]" with the job's name, obviously). If the handler
isn't defined then a default handler (imaginatively called `default_handler`)
is called.

Each handler is passed a `Page` object, which corresponds to the web page
retrieved, and a `Job` object (corresponding to the Job being run). Because you
can assign arbitrary attributes to the `Job` object when it is created, this is
a great way of passing extra information around between handlers. For example,
say you are scraping a movie site, you could give a `Job` a "title" attribute
when it is created, so the handler which will be run later on knows the title
of the movie it is dealing with.

Here is the most basic possible scraper::

    from aioscraper import BaseCrawler

    class MyCrawler(BaseCrawler):
        initial_urls = ['http://en.wikipedia.org/']

        def handle_initial(self, page, job):
            print(page.text)

    bot = MyCrawler()
    bot.run()

It simply prints out the source code for Wikipedia's home page.

To queue new jobs to be handled, a handler simply needs to yield a `Job`
object. Here is an extended example that uses BeautifulSoup to extract all the
sub-pages from Wikipedia's home page and then scrape them::

    from aioscraper import BaseCrawler, Job
    from urllib.parse import urljoin


    class MyCrawler(BaseCrawler):
        initial_urls = ['http://en.wikipedia.org/']

        def handle_initial(self, page, job):
            for link in page.soup.find_all('a'):
                href = link['href']

            if href.startswith('/'):
                href = urljoin('http://en.wikipedia.org/', href)

            # Only get pages which are on the "en.wikipedia.org" domain
            if 'en.wikipedia.org' in href:
                new_job = Job('page', url=href)
                yield new_job

    bot = MyCrawler()
    bot.run()




