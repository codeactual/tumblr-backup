import os
import sys
import unittest

root_dir = os.path.dirname(os.path.abspath(__file__)) + '/..'

sys.path.append(root_dir + '/src')
import tumblrbackup as tb
import normalize4yql as normalize

def get_test_page():
    config = tb.get_config('config-test.json')
    limit = 1
    offset = 1
    return tb.get_posts(config['url'], config['api_key'], limit, offset)

class TumblrBackupTestCase(unittest.TestCase):
    def test_get_config(self):
        config = tb.get_config('config-dist.json')
        self.assertEqual('my.tumblr.com', config['url'])
        self.assertEqual('myApiKey', config['api_key'])
        self.assertEqual('format', config['strip_metadata'][0])

    def test_get_posts(self):
        page = get_test_page()
        self.assertEqual(1, len(page['posts']))
        self.assertEqual(3, page['pages_left'])
        self.assertEqual('<p>post3 post1</p>', page['posts'][0]['body'])
        self.assertEqual(11084927889, page['posts'][0]['id'])
        self.assertListEqual(['tag3', 'tag1'], page['posts'][0]['tags'])
        self.assertEqual(1317865857, page['posts'][0]['timestamp'])
        self.assertEqual('title3 title1', page['posts'][0]['title'])
        self.assertEqual('text', page['posts'][0]['type'])

    def test_strip_metadata(self):
        page = get_test_page()
        self.assertTrue('type' in page['posts'][0])
        self.assertFalse('id' not in page['posts'][0])
        self.assertFalse('tags' not in page['posts'][0])

    def test_backup(self):
        expected = open(root_dir + '/test/fixture/backup.json').read().rstrip()
        actual = tb.backup('config-test.json')
        self.assertEqual(expected, actual)

class Normalize4YqlTestCase(unittest.TestCase):
    def test_output(self):
        expected = open(root_dir + '/test/fixture/backup-normalized4yql.json').read().rstrip()
        actual = normalize.normalize(root_dir + '/test/fixture/backup-alltypes.json', 'http://domain.com')
        self.assertEqual(expected, actual)
