import csv, os, unittest
import utils.logger, utils.csv

class TestCSV(unittest.TestCase):
    def setUp(self):
        if os.path.exists("utils/util_csv/selftest.csv"):
            os.remove("utils/util_csv/selftest.csv")
        
        self.ds = utils.csv.Datastore("selftest")

    def test_doesnotexist(self):
        self.assertFalse(self.ds.exists(99))

    def test_blankread(self):
        self.assertEqual(None, self.ds.read(98))

    def test_addandremove(self):
        self.assertFalse(self.ds.exists(1))
        self.ds.update(1, {'id': 'test'})
        self.assertTrue(self.ds.exists(1))
        self.assertEqual("test", self.ds.read(1)['id'])
        self.ds.remove(1)
        self.assertFalse(self.ds.exists(1))

    def test_saveandload(self):
        self.ds.update(2, {'id': '2', 'val': "testing"})
        self.ds.update(4, {'id': '4', 'val': "yippee"})
        self.ds.save()
        self.ds.load()
        self.assertEqual("testing", self.ds.read(2)['val'])