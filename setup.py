#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cleverapi",
    version="0.3.4",
    author="Oncecreated",
    description="Python Clever Api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oncecreated/cleverapi",
    packages=find_packages(),
    install_requires=['requests', "aiohttp"],
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    )
)
