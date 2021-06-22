from setuptools import find_packages
from setuptools import setup

from trie import __version__

setup(
    name='trie',
    version=__version__,
    url='https://github.com/walkingpendulum/trie',
    packages=find_packages(exclude=('tests',)),
    package_dir={'trie': 'trie'},
    install_requires=[
    ],
)
