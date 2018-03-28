#!/usr/bin/python
# -*- coding: utf-8 -*-
#!Design by CHN-STUDENT
#!Useing on Python 3

import codecs
from setuptools import setup


setup(
    name="srun-cli",
    version="0.0.4",
    license='http://www.apache.org/licenses/LICENSE-2.0',
    description="A Command line interface for Srun3k Client for HAUT",
    author='CHN-STUDENT',
    author_email='chn-student@outlook.com',
    url='https://github.com/CHN-STUDENT/srun-cli',
    packages=['srun'],
    install_requires=[],
    entry_points="""
    [console_scripts]
    srun = srun.local:main
    srun-cli = srun.local:main
    """,
)
