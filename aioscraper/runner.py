"""
Similar to scrapy's ability to give you a shell to test your spider, you're
also able to test handlers using the runner module.
"""

import importlib
import readline
import sys
import requests
from bs4 import BeautifulSoup

from .models import Job, Page



def test_shell(url, headers=None):
    """
    Allow the user to interractively try out their BeautifulSoup selectors
    and so on.
    """
    r = requests.get(url, headers=headers)

    # Populate the page representation
    page = Page(url)
    page.status = r.status_code
    page.content = r.content
    page.text = r.text
    page.soup

    # Set up an interactive shell 
    namespace = globals().copy()
    namespace.update(locals())

    try:
        import IPython
        interact = IPython.embed
    except ImportError:
        import code
        shell = code.InteractiveConsole(namespace)
        interact = shell.interact

    print('Some of the variables you have access to:')
    print('-----------------------------------------')
    print('BeautifulSoup -', BeautifulSoup)
    print('Job -', Job)
    print('Page -', Page)
    print('page -', page)
    print('requests -', requests)
    print('url -', repr(url))
    print()

    interact()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = 'http://google.com/'
    test_shell(url)
