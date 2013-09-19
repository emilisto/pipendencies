import xmlrpclib
from distutils.version import LooseVersion
from pip.req import parse_requirements, InstallRequirement
from enum import Enum

PYPI_INDEX = 'http://pypi.python.org/pypi'

class Requirement(InstallRequirement):

    class Status(Enum):
        unspecified = 1
        invalid     = 2
        uptodate    = 3
        outdated    = 4

    status           = None
    latest_version   = None
    required_version = None

    def _fetch_pypi_version(self):
        client = xmlrpclib.ServerProxy(PYPI_INDEX)
        self._pypi_versions = [ LooseVersion(v) for v in client.package_releases(self.name) ]
        return self.status is self.Status.uptodate

    @property
    def specified_version(self):
        versions = list(self.absolute_versions)
        return versions[0] if len(versions) > 0 else None

    @property
    def pypi_versions(self):
        if not hasattr(self, '_pypi_versions'):
            self.check()
        return self._pypi_versions

    @property
    def latest_version(self):
        return self.pypi_versions[0]

    @property
    def status(self):
        if self.specified_version is None:
            return Requirement.Status.unspecified
        elif self.specified_version not in self.pypi_versions:
            return Requirement.Status.invalid
        elif self.specified_version < self.latest_version:
            return Requirement.Status.outdated
        else:
            return Requirement.Status.uptodate

    @classmethod
    def from_line(cls, line):
        req = super(cls, Requirement).from_line(line)
        req._fetch_pypi_version()
        return req

def check_requirements(requirements):

    jobs = check_requirements(requirements)
    gevent.joinall(jobs)
    results = [ job.value for job in jobs ]
    print results

    # Determine packages to check
    #jobs, requirements = [], []
    #for req in reqs:
        #try:
            #version = req.absolute_versions.pop()
            #jobs.append(gevent.spawn(lambda p: (p, fetch_versions(p)[0],), p))
        #except IndexError:
            #pass
    #interact()

    ## Determine latest versions from PyPi index
    #available = [ job.value for job in jobs ]
    #print available
