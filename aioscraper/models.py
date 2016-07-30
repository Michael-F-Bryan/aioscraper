"""
The core data structures used to represent pages and jobs.
"""

from bs4 import BeautifulSoup


class Page:
    """
    A representation of a web page response.
    """
    def __init__(self, url):
        self.url = url
        self.status = None
        self.text = ''
        self.content = b''
        self._soup = None
        
    @property
    def soup(self):
        """
        Lazily create a BeautifulSoup object. Because using BeautifulSoup 
        might not be necessary we implement it as a property that will 
        generate the soup and cache it the first time someone accesses the
        soup property.
        """
        if self._soup is None:
            self._soup = BeautifulSoup(self.text, 'html.parser')
            
        return self._soup
        
    def __repr__(self):
        return '<{}: url={}>'.format(
                self.__class__.__name__,
                self.url if len(self.url) < 37 else self.url[:37] + '...')
        

class Job:
    def __init__(self, name, url, method='GET', headers=None, cookies=None):
        self.name = name
        self.url = url
        self.method = method
        self.headers = headers
        self.cookies = cookies
        
    def __repr__(self):
        return '<{}: name="{}" url={}>'.format(
                self.__class__.__name__,
                self.name,
                self.url if len(self.url) < 27 else self.url[:27] + '...')        
