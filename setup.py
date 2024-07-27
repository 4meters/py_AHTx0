#!/usr/bin/env python

import os
import re
import sys
from setuptools import setup

here = os.path.dirname(__file__)



def _read_version():
    with open(os.path.join(here, 'py_AHTx0', '__init__.py')) as code:
        contents = code.read()
    match = re.search(r'__version__\s*=\s*["\'](.*?)["\']', contents)
    return match.group(1)


needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []
test_deps = [
    'pytest>=3.1',
    'pytest-cov'
]

version = _read_version()

# Read the contents of your README file
with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="py_AHTx0",
    version=version,
    author="Kattni Rembor, Marcin Ryznar",
    author_email="poczta321123@onet.pl",
    description="A library to drive a AHT10 or AHT20 temperature, humidity sensor over I2C",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/4meters/py_AHTx0",
    license="MIT",
    keywords=["raspberry pi", "orange pi", "banana pi", "rpi", "AHT10", "AHT20", "i2c", "temperature", "humidity", "smbus2"],
    packages=['py_AHTx0'],
    install_requires=["smbus2"],
    setup_requires=pytest_runner,
    tests_require=test_deps,
    python_requires=">=3.6, <4",
    extras_require={
        'docs': [
            'sphinx>=1.5.1'
        ],
        'qa': [
            'rstcheck',
            'flake8'
        ],
        'test': test_deps
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Topic :: Education",
        "Topic :: System :: Hardware",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12"
    ]
)
