"""Setup script for hex2words"""
from setuptools import setup

setup(
    name="hexwordify",
    description="Turn hexadecimal strings to readable words.",
    version="0.0.2",

    author="Dimitris Zervas",
    author_email="dzervas@dzervas.gr",

    packages=["hexwordify"],

    entry_points={
        "console_scripts": [
            "hexwordify=hexwordify.__main__:main",
        ],
    },
)
