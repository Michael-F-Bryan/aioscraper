from setuptools import setup


setup(
        name='aioscraper',
        author='Michael F Bryan',
        author_email='michaelfbryan@gmail.com',
        version='0.1.0',

        packages=['aioscraper'],

        install_requires=[
            'aiohttp',
            'bs4',
            'requests',
            ],
        )
