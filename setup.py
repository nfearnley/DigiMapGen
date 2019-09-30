import os
import codecs

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), "r") as f:
        return f.read()


setup(
    name="digimapgen",
    version="0.2.2",
    description="It generates maps.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    keywords="",
    author="DigiDuncan",
    author_email="digiduncan@gmail.com",
    url="https://github.com/DigiDuncan/DigiMapGen",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "colored"
    ],
    python_requires=">=3",
    classifiers=[
    ],
    entry_points={
        "console_scripts": [
            "digimapgen = main:main"
        ]
    }
)
