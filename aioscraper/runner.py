"""
Similar to scrapy's ability to give you a shell to test your spider, you are
also able to test handlers in an interactive environment.
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
    try:
        r = requests.get(url, headers=headers)
    except requests.RequestException as e:
        print('An error occurred while fetching "{}"'.format(url))
        print()
        print(e)
        sys.exit(1)

    # Populate the page representation
    page = Page(url)
    page.status = r.status_code
    page.content = r.content
    page.text = r.text
    page.soup

    # Set up an interactive shell 
    namespace = globals().copy()
    namespace.update(locals())

    # First check to see if the user has IPython installed, and try to use
    # That for our interactive shell
    try:
        import IPython
        interact = IPython.embed
    except ImportError:
        # Otherwise fall back to a plain Python one
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
    # A simple bit of code that will take the first command line argument
    # And run our interactive shell using whatever is retrieved.
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = 'http://google.com/'
    test_shell(url)
