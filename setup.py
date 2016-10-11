#!/usr/bin/env python

import os
from setuptools import setup, find_packages

import harness

setup(
    name='testharness',
    version=harness.__version__,
    description='Test Harness tool for <your-zeromq-application-name>',
    author='Deep Aggarwal',
    author_email='deep.uiuc@gmail.com',
    maintainer='Deep Aggarwal',
    maintainer_email='deep.uiuc@gmail.com',
    url='https://github.com/deep4788/testHarness.git',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'harness = harness.script:main',
        ]
    },
)
