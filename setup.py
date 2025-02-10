"""setup"""

from os import getenv
import pathlib
from setuptools import setup
from setuptools import find_packages

VERSION = getenv("VERSION_VAR") or pathlib.Path("version.txt").read_text(encoding="utf-8").strip()

HERE = pathlib.Path(__file__).parent
LONG_DESCRIPTION = (HERE / "README.md").read_text()
INSTALL_REQUIRES = [f"{line}" for line in (HERE / "requirements.txt").read_text().splitlines()]
DOWNLOAD_URL = f"https://github.com/bikram990/certbot-dns-dynu/archive/refs/tags/{VERSION}.tar.gz"

# https://setuptools.pypa.io/en/latest/references/keywords.html
setup(
    name="certbot-dns-dynu",
    version=VERSION,
    description="Dynu DNS Authenticator plugin for Certbot",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/bikram990/certbot-dns-dynu",
    download_url=DOWNLOAD_URL,
    author="Bikramjeet Singh",
    license="Apache License 2.0",
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Plugins",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Security",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    package_dir={"": "src"},
    packages=find_packages(
        where="src",
        include=["certbot_dns_dynu", "certbot_dns_dynu.*"],
        exclude=["tests"],
    ),
    install_requires=INSTALL_REQUIRES,
    # extras_require={
    #     'docs': docs_extras,
    # },
    entry_points={
        "certbot.plugins": [
            "dns-dynu = certbot_dns_dynu.dns_dynu:Authenticator",
        ],
    },
)
