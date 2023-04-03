# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open("README.rst") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="nba_stats_tracker",
    version="0.1.0",
    description="nba_stats_tracker package",
    long_description=readme,
    author="Behzad Amiri",
    author_email="behzad.amiri@gmail.com",
    url="",
    license=license,
    packages=find_packages(exclude=("tests", "docs")),
)
