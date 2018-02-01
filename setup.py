"""Setup script for hex2words"""
from setuptools import setup

setup(
    name="hex2words",
    description="Turn hexadecimal strings to readable words.",
    version="0.0.1",

    author="Dimitris Zervas",
    author_email="dzervas@dzervas.gr",

    packages=["hex2words"],

    # scripts=["hex2words=hex2words.py"]
    entry_points={
        "console_scripts": [
            "hex2words=hex2words.__main__:main",
        ],
    },
)
