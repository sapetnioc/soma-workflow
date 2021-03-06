
version_major = 2
version_minor = 7
version_micro = 0
version_extra = ''

# Format expected by setup.py and doc/source/conf.py: string of form "X.Y.Z"
__version__ = "%s.%s.%s%s" % (version_major,
                              version_minor,
                              version_micro,
                              version_extra)
CLASSIFIERS = ["Development Status :: 1 - Planning",
               "Environment :: Console",
               "Operating System :: OS Independent",
               "Programming Language :: Python",
               "Topic :: Scientific/Engineering",
               "Topic :: Utilities"]

description = 'Soma-Workflow. A unified and simple interface to parallel computing resource'

long_description = """
=============
Soma-Workflow
=============

A unified and simple interface to parallel computing resource
"""

# versions for dependencies
SPHINX_MIN_VERSION = '1.0'

# Main setup parameters
NAME = 'soma-workflow'
ORGANISATION = "CEA"
MAINTAINER = "CEA"
MAINTAINER_EMAIL = ""
DESCRIPTION = description
LONG_DESCRIPTION = long_description
URL = "http://brainvisa.info/soma-workflow"
DOWNLOAD_URL = "http://brainvisa.info/soma-workflow"
LICENSE = "CeCILL-B"
CLASSIFIERS = CLASSIFIERS
AUTHOR = "Soma-Workflow developers"
AUTHOR_EMAIL = ""
PLATFORMS = "OS Independent"
PROVIDES = ["soma-workflow"]
REQUIRES = []
EXTRA_REQUIRES = {"doc": ["sphinx>="+SPHINX_MIN_VERSION]}

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

DB_VERSION = '1.1'
