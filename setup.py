from setuptools import setup


setup(
        name='aioscraper',
        author='Michael F Bryan',
        author_email='michaelfbryan@gmail.com',
        version='version=0.1.1',

        packages=['aioscraper'],

        install_requires=[
            'aiohttp',
            'bs4',
            'requests',
            ],
        )
