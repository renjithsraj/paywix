#!/usr/bin/pythoni

from setuptools import setup, find_packages
from os import path

p = path.abspath(path.dirname(__file__))
with open(path.join(p, 'README.rst')) as f:
    README = f.read()

setup(
    name='paywix',
    version='4.3.4',
    description='Multipayment gateway wrapper for Django',
    long_description=README,
    long_description_content_type='text/markdown',
    install_requires=[
        "django",
        "pycrypto"
    ],
    url='https://github.com/renjithsraj/paywix',
    maintainer='Renjith S Raj',
    maintainer_email='renjithsraj@live.com',
    download_url='',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          'Framework :: Django :: 2.2',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.7',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Software Development'
    ],
)
