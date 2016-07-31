"""
A web scraping framework constructed similarly to the `grab` or `scrapy`
libraries, but using Python's `asyncio` library.
"""

from .models import Page, Job
from .scraper import BaseCrawler

__version__ = '__version = '0.1.1''

__all__ = [
        'Page', 'Job', 'BaseCrawler',
        ]
