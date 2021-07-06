#! /usr/bin/env python3
#
# pymetar
# (c) 2002 Tobias Klausmann
# (c) 2002 Jerome Alet <alet@librelogiciel.com>
# You're welcome to redistribute this software under the
# terms of the GNU General Public Licence version 2.0
# or, at your option, any higher version.
#
# You can read the complete GNU GPL in the file COPYING
# which should come along with this software, or visit
# the Free Software Foundation's WEB site http://www.fsf.org
#
# $Id: $

import pymetar
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymetar",
    version=pymetar.__version__,
    author="Tobias Klausmann",
    author_email="klausman-pymetar@schwarzvogel.de",
    description="Pymetar is a python module and command line tool that fetches and parses METAR reports",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.schwarzvogel.de/software-pymetar.shtml",
    packages=setuptools.find_packages(),
    py_modules=["pymetar"],
    scripts=["bin/pymetar"],
    classifiers=(
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)", 
   "Operating System :: OS Independent",)
)
