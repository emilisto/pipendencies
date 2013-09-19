import xmlrpclib

from distutils.version import LooseVersion
from pip.req import parse_requirements, InstallRequirement
from enum import Enum

class Requirement(InstallRequirement):

    PYPI_INDEX = 'http://pypi.python.org/pypi'

    class Status(Enum):
        unspecified = 1
        invalid     = 2
        uptodate    = 3
        outdated    = 4

    status           = None
    latest_version   = None
    required_version = None

    def _fetch_pypi_version(self):
        client = xmlrpclib.ServerProxy(self.PYPI_INDEX)

        # show_hidden=True gives us older versions of packages as well, which
        # is good since it will help us in telling whether a specified version
        # is invalid or just outdated.
        self._pypi_versions = list(client.package_releases(self.name, True))

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
        try:
            return self.pypi_versions[0]
        except IndexError:
            return None

    @property
    def status(self):
        if self.specified_version is None:
            return Requirement.Status.unspecified
        elif self.specified_version not in self.pypi_versions:
            return Requirement.Status.invalid
        elif LooseVersion(self.specified_version) < LooseVersion(self.latest_version):
            return Requirement.Status.outdated
        else:
            return Requirement.Status.uptodate

    @classmethod
    def from_line(cls, line):
        req = super(cls, Requirement).from_line(line)
        req._fetch_pypi_version()
        return req
