import bootstrap
import normalize4yql as normalize
import unittest

class Normalize4YqlTestCase(unittest.TestCase):
    def test_output(self):
        expected = open(bootstrap.root_dir + '/test/fixture/backup-normalized4yql.json').read().rstrip()
        actual = normalize.normalize(bootstrap.root_dir + '/test/fixture/backup-alltypes.json', 'http://domain.com')
        self.assertEqual(expected, actual)

