#!/usr/bin/pythoni

from setuptools import setup, find_packages
from os import path

p = path.abspath(path.dirname(__file__))
with open(path.join(p, 'README.rst')) as f:
    README = f.read()

setup(
    name='paywix',
    version='2.0',
    author="Renjith S Raj",
    author_email="renjithsraj@live.com",
    description='Paywix is a payment gateway wrapper is a application that integrates multiple payment '
                'gateways into a single platform. It simplifies the processing  payments by '
                'providing a unified API that allows merchants/Customer to access multiple payment gateways '
                'without having to write separate code for each gateway. This increases the ease of '
                'use and versatility for the merchants, and reduces the time and cost of development.',
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
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    keywords='payment gateway, payu, paytm, paywix, payment gateway wrapper, gateway',
)
