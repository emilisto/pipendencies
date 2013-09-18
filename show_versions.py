#!/usr/bin/env python

"""
Syntax: $0 <package>

Prints the available in versions in PyPi for <package>
"""

import sys
import xmlrpclib

package = sys.argv.pop()
client = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')
print "%s: %s" % (package, client.package_releases(package),)
