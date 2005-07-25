#! /usr/bin/env python
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

from distutils.core import setup

import pymetar

setup(name = "pymetar", version = pymetar.__version__,
      license = "GNU GPL",
      description = pymetar.__doc__,
      author = "Tobias Klausmann",
      author_email = "klausman-pymetar@schwarzvogel.de",
      url = "http://www.schwarzvogel.de/software-pymetar.shtml",
      packages= [ "" ],
      scripts = [ "bin/pymet2.py" ])
