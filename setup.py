#!/usr/bin/pythoni

from setuptools import setup, find_packages
from os import path

p = path.abspath(path.dirname(__file__))
with open(path.join(p, 'README.rst')) as f:
    README = f.read()

setup(
    name='paywix',
    version='1.2.0',
    description='Multipayment gateway wrapper for Django',
    long_description=README,
    long_description_content_type='text/markdown',
    install_requires=[
    ],
    url='https://github.com/renjithsraj/paywix',
    maintainer='Renjith S Raj',
    maintainer_email='renjithsraj@live.com',
    download_url='',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
