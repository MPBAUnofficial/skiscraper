import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='skiscraper',  # uhuh such a great name
    version=open('VERSION').read().strip('\n'),
    description='Find informations about ski centers in Trentino',
    long_description=README,
    license='FreeBSD License',
    url='',
    author='Marco Dallagiacoma',
    author_email='dallagiac@fbk.eu',
    packages=['skiscraper', 'skiscraper.skicenters'],
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: FreeBSD License',  # cosi tanto per
        'Operating System :: OS Indipendent',
    ],
    install_requires=['requests', 'BeautifulSoup4'],
    zip_safe=False,
)

