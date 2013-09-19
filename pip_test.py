#!/usr/bin/env python

# Hohoho
from gevent import monkey
monkey.patch_all()

import sys
import gevent
from distutils.version import StrictVersion, LooseVersion
from interact import interact


"""
Good docs:

    - http://docs.python.org/2/distutils/apiref.html#module-distutils.version

"""

def playaround():
    import pip
    from pip.index import PackageFinder
    from pip.req import InstallRequirement, RequirementSet

    req = InstallRequirement.from_line("django-hoptoad", None) 

    finder = PackageFinder(find_links=[], index_urls=["http://pypi.python.org/simple/"])
    ret = finder.find_requirement(req, False)
    print ret
    print type(ret)

    interact()

import xmlrpclib
from pprint import pprint
def find_versions(package):
    client = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')
    return [ LooseVersion(v) for v in client.package_releases(package) ]

from pip.req import parse_requirements, InstallRequirement
def find_outdated(requirements):
    # Find specified versions in requirements.txt
    reqs = [ InstallRequirement.from_line(req) for req in requirements ]
    packages = [ req.name for req in reqs ]
    interact()

    # Determine latest versions from PyPi index
    jobs = [ gevent.spawn(lambda p: (p, find_versions(p)[0],), p) for p in packages ]
    gevent.joinall(jobs)
    available = [ job.value for job in jobs ]
    print available

def find_outdated_test():
    with open('./sample_requirements.txt') as f:
        find_outdated(f.readlines())

def find_versions_test():
    packages = [ 'Django', 'requests', 'pip' ]

    jobs = [ gevent.spawn(lambda p: (p, find_versions(p),), p) for p in packages ]
    gevent.joinall(jobs)
    print [ job.value for job in jobs ]

def test_versions():
    ver1 = LooseVersion('2013d')
    ver2 = LooseVersion('2012d')
    print "ver1 < ver2: %s" % (ver1 > ver2)

#find_versions_test()
#test_versions()
find_outdated_test()
