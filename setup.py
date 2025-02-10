#! /usr/bin/env python
from os import path
from setuptools import setup
from setuptools import find_packages

version = "0.0.4"

with open('README.md') as f:
    long_description = f.read()

install_requires = [
    'acme>=2.0.0',
    'certbot>=2.0.0',
    'dns-lexicon>=3.11.7',
    'dnspython',
    'mock',
    'setuptools',
    'requests'
]

here = path.abspath(path.dirname(__file__))

setup(
    name='certbot-dns-dynu',
    version=version,

    description="Dynu DNS Authenticator plugin for Certbot",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bikram990/certbot-dns-dynu',
    download_url='https://github.com/bikram990/certbot-dns-dynu/archive/refs/tags/' + version +'.tar.gz',
    author="Bikramjeet Singh",
    license='Apache License 2.0',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],

    packages=find_packages(),
    install_requires=install_requires,

    # extras_require={
    #     'docs': docs_extras,
    # },

    entry_points={
        'certbot.plugins': [
            'dns-dynu = certbot_dns_dynu.dns_dynu:Authenticator',
        ],
    },
    test_suite='certbot_dns_dynu',
)
