#!/usr/bin/python
# -*- coding: utf-8 -*-
#!Design by CHN-STUDENT
#!Using on Python 3 and Python2.7

import codecs
from setuptools import setup


setup(
    name="srun-cli",
    version="0.1.1",
    license='http://www.apache.org/licenses/LICENSE-2.0',
    description="A Command line interface for Srun3k Client for HAUT",
    author='CHN-STUDENT',
    author_email='chn-student@outlook.com',
    url='https://github.com/CHN-STUDENT/srun-cli',
    packages=['srun'],
    install_requires=['six'],
    entry_points="""
    [console_scripts]
    srun = srun.local:main
    srun-cli = srun.local:main
    """,
)
