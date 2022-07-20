# -*- coding: utf-8 -*-
from pathlib import Path
from setuptools import find_packages
from setuptools import setup


version = "3.2.0"

this_directory = Path(__file__).parent
long_description = (
    (this_directory / "README.md").read_text()
    + "\n\n"
    + (this_directory / "CHANGES.md").read_text()
)


setup(
    name="collective.behavior.relatedmedia",
    version=version,
    description="Adds Various configuration fields and viewlets to manage "
    "and show content related images and attachments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Addon",
        "Framework :: Plone",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="plone richmedia relatedmedia",
    author="petschki",
    author_email="peter.mathis@kombinat.at",
    url="https://github.com/kombinat/collective.behavior.relatedmedia",
    license="gpl",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["collective", "collective.behavior"],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=[
        "setuptools",
        # -*- Extra requirements: -*-
        "plone.api",
        "plone.behavior",
        "plone.app.dexterity",
    ],
    extras_require={
        "test": [
            "plone.app.testing[robot]",
            "plone.app.robotframework",
            "plone.app.contenttypes",
            "robotframework-selenium2library",
            "robotframework-selenium2screenshots",
        ],
    },
    entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
)
