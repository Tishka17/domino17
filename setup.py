#!/usr/bin/env python3

from setuptools import setup

setup(
    name='domino17',
    description='Proper python bindings for the Domino API.',
    version='0.1',
    packages=['domino17', 'domino17.models'],
    install_requires=[
        'requests',
        'dataclass_factory==2.*',
        'dataclasses;python_version<"3.7"',
    ],
)
