#!/usr/bin/env python

# Hohoho
from gevent import monkey
monkey.patch_all()

#import gevent
#from interact import interact
#import sys

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

def find_latest_release(package):
    import xmlrpclib
    from pprint import pprint

    client = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')
    releases = client.package_releases(package)
    pprint(releases)

from pip.req import parse_requirements, InstallRequirement
def parse_reqs(reqs):
    reqs = list(parse_requirements(reqfile))
    interact()
    print reqs
    #return [ req.name for req in  ]

def find_outdated(requirements):
    reqs = [ InstallRequirement.from_line(req) for req in requirements ]
    names = [ req.name for req in reqs ]
    print reqs
    print names

#find_releases()

with open('./requirements.txt') as f:
    find_outdated(f.readlines())
#print parse_reqs('./requirements.txt')
