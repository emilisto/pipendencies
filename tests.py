import unittest
import xmlrpclib
from mock import patch
from pprint import pprint

from pipendencies.requirements import Requirement

class TestRequirements(unittest.TestCase):

    @patch('xmlrpclib.ServerProxy')
    def test_check_requirement(self, mock_xmlrpc):
        m = mock_xmlrpc.return_value
        m.package_releases.return_value = ['1.5.4', '1.5.3', '1.5.2', '1.5.1',]

        req = Requirement.from_line('Django==1.5.2')
        self.assertEquals(req.status, Requirement.Status.outdated)

        req = Requirement.from_line('Django==1.5.4')
        self.assertEquals(req.status, Requirement.Status.uptodate)

        req = Requirement.from_line('Django==1.5.5')
        self.assertEquals(req.status, Requirement.Status.invalid)
        req = Requirement.from_line('Django==1.5.0')
        self.assertEquals(req.status, Requirement.Status.invalid)

        req = Requirement.from_line('Django>=1.5.0')
        self.assertEquals(req.status, Requirement.Status.unspecified)

        req = Requirement.from_line('Django')
        self.assertEquals(req.status, Requirement.Status.unspecified)

        m.package_releases.return_value = []
        req = Requirement.from_line('Django>=1.5.0')
        self.assertEquals(req.latest_version, None)

if __name__ == '__main__':
    unittest.main()
