# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = "3.0.0"


def read_file(fname):
    with open(fname) as f:
        return f.read()


setup(
    name="collective.behavior.relatedmedia",
    version=version,
    description="Adds Various configuration fields and viewlets to manage "
    "and show content related images and attachments",
    long_description=read_file("README.md") + "\n\n\n" + read_file("CHANGES.md"),  # noqa
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
