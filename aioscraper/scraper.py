"""
A base scraper that all scrapers inherit from.
"""

import asyncio
import sys
import logging
import inspect
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import aiohttp

from .models import Page, Job


class BaseCrawler:
    """
    The base crawler class. It runs the event loop and will handle all job
    by running their associated job handlers.
    """
    initial_urls = ['http://google.com/']
    
    def __init__(self, config=None):
        self.config = config or {}
        self.loop = asyncio.get_event_loop()
        self.tasks = []
        
        # Use a semaphore for rate limiting so we only have a set number of
        # concurrent connections
        self.lock = asyncio.Semaphore(self.config.get('max-connections', 10),
                                      loop=self.loop)
        
        # Set up logging
        if 'logger' in self.config:
            # Check whether the user gave us a logger to work with
            self.logger = self.config['logger']
        else:
            # Otherwise, make one
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(self.config.get('log-level', logging.DEBUG))
            
            log_file = self.config.get('log-file', 'stderr')

            if log_file == 'stdout':
                handler = logging.StreamHandler(sys.stdout)
            elif log_file == 'stderr':
                handler = logging.StreamHandler(sys.stderr)
            else:
                handler = logging.FileHandler(log_file)

            self.logger.handlers.clear()
            
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s: %(message)s',
                datefmt='%Y/%m/%d %I:%M:%S %p'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
    def prepare(self):
        """
        A function run just before starting the event loop to set up the 
        crawler. Do stuff like initializing variables and setting up database
        connections or caches here.
        """
        self.base_url = 'http://google.com/'
    
    async def get_page(self, url, method='GET', headers=None, cookies=None):
        """
        Retrieve a web page asynchronously.
        """
        with (await self.lock):
            async with aiohttp.ClientSession(headers=headers, cookies=cookies) as session:
                async with session.request(method, url) as resp:
                    page = Page(url)
                    page.status = resp.status
                    page.text = await resp.text()
                    page.content = await resp.read()
                    return page
                
    async def handle(self, job):
        """
        Fetch the web page specified by a job, then run its corresponding job
        handler. If the job handler isn't defined then run default_handler().

        If the job handler yields anything then assume it is another Job to 
        be queued, and queue it to be handled soon.
        """
        self.logger.debug('Fetching %s', job.url)
        page = await self.get_page(
                job.url,
                job.method,
                job.headers,
                job.cookies)
        self.logger.debug('Page "%s" is %d bytes', job.url, len(page.content))
        
        # Get the job handler
        handler_name = 'handle_{}'.format(job.name)
        handler = getattr(self, handler_name, self.default_handler)
                    
        self.logger.debug('Using %s() to handle job: %r', handler.__name__, job)
        
        # Do something with the data received
        if inspect.isgeneratorfunction(handler):
            for task in handler(page, job):
                self.queue(task)
        else:
            result = handler(page, job)
            
            if result is not None:
                self.queue(result)
            
    def handle_initial(self, page, job):
        for link in page.soup.find_all('a'):
            href = link['href']
            
            if href.startswith('/'):
                href = urljoin(self.base_url, href)

            new_job = Job('blah', href)
            yield new_job
    
    def default_handler(self, page, job):
        """
        A default handler that just raises a NotImplementedError when called.
        """
        raise NotImplementedError('Handler not implemented for job: {}'.format(job))
        
    def queue(self, job):
        """
        Queue a job to be handled later, returning a asyncio.Task.
        """
        task = asyncio.ensure_future(self.handle(job), loop=self.loop)
        self.tasks.append(task)
        self.logger.debug('Queued a job, %r', job)
        return task

    def run(self):
        """
        Run the prepare() function, then start the event loop and keep running
        it until all tasks are either done or cancelled.
        """
        self.prepare()
        
        for url in self.initial_urls:
            some_task = Job('initial', url)
            self.queue(some_task)
        
        # While all tasks aren't either cancelled or done, run the loop until
        # All currently queued tasks are done. Then check again.
        while not all(t.cancelled() or t.done() 
                for t in asyncio.Task.all_tasks(loop=self.loop)):
            self.loop.run_until_complete(asyncio.gather(*self.tasks))
