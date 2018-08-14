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

setuptools.setup(
    name="pymetar",
    version=pymetar.__version__,
    author="Tobias Klausmann",
    author_email="klausman-pymetar@schwarzvogel.de",
    description=pymetar.__doc__,
    url="http://www.schwarzvogel.de/software-pymetar.shtml",
    license="GNU GPL",
    packages=setuptools.find_packages(),
    py_modules=["pymetar"],
    scripts=["bin/pymetar"],
    data_files=[("share/doc/pymetar-%s" % pymetar.__version__,
                 ['README.md', 'COPYING', 'THANKS', 'librarydoc.txt']),
                ("share/man/man1", ['pymetar.1'])]
)
