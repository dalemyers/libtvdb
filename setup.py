#!/usr/bin/env python3

from os import path

from setuptools import setup, find_packages

import libtvdb

def run_setup():
    """Run package setup."""
    here = path.abspath(path.dirname(__file__))

    # Get the long description from the README file
    try:
        with open(path.join(here, 'README.md')) as f:
            long_description = f.read()
    except:
        # This happens when running tests
        long_description = None

    setup(
        name='libtvdb',
        version=libtvdb.__version__,
        description='An API wrapper around the TVDB.',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url='https://github.com/dalemyers/libtvdb',
        author='Dale Myers',
        author_email='dale@myers.io',
        license='MIT',
        install_requires=[],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.7',
            'Topic :: Software Development :: Libraries'
        ],

        keywords='tvdb, tv, tv database',
        packages=find_packages(exclude=['docs', 'tests'])
    )

if __name__ == "__main__":
    run_setup()
