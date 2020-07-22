# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = '2.1.3'


def read_file(fname):
    with open(fname) as f:
        return f.read()


setup(name='collective.behavior.relatedmedia',
      version=version,
      description="Adds Various configuration fields and viewlets to manage "
                  "and show content related images and attachments",
      long_description=read_file("README.rst") + "\n" + read_file("CHANGES.rst"),  # noqa
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: Addon",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='',
      author='',
      author_email='',
      url='https://github.com/kombinat/collective.behavior.relatedmedia',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.behavior'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'plone.api',
          'plone.behavior',
          'plone.app.dexterity',
      ],
      extras_require={
        'test': [
            'plone.app.testing[robot]',
            'plone.app.robotframework',
            'plone.app.contenttypes',
            'robotframework-selenium2library',
            'robotframework-selenium2screenshots',
        ],
    },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
