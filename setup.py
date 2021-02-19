#!/usr/bin/pythoni

from setuptools import setup, find_packages
from os import path

p = path.abspath(path.dirname(__file__))
with open(path.join(p, 'README.rst')) as f:
    README = f.read()

setup(
    name='paywix',
    version='1.4.0',
    author="Renjith S Raj",
    author_email="renjithsraj@live.com",
    description='Paywix is a light weight payment processing sdk for python based applications.',
    long_description=README,
    long_description_content_type='text/markdown',
    install_requires=[
        'requests'
    ],
    url='https://github.com/renjithsraj/paywix',
    maintainer='Renjith S Raj',
    maintainer_email='renjithsraj@live.com',
    download_url='',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    keywords='payment processing, payu, python payment gateway wrapper, cashfree, paytm, etc',
)
