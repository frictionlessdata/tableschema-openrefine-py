from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='jsontableschema-openrefine',
    version='0.0.1',
    description='Import and export JSON Table Schema into OpenRefine',
    long_description=long_description,

    url='https://github.com/okfn/jsontableschema-openrefine-py',

    author='Open Knowledge Foundation',
    author_email='info@okfn.org',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Topic :: Utilities',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
    ],

    keywords='data dataprotocols jsontableschema openrefine datascience',

    packages=find_packages(exclude=['tests']),
    entry_points='''
        [console_scripts]
        jsontableschema-openrefine = jsontableschema.plugins.openrefine.cli:cli
    ''',

    install_requires=[
        'click >= 5.0',
        'requests >= 2.0',
        'six >= 1.0',
    ],
)
