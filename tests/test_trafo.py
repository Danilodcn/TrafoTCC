from unittest import TestCase
import os

class TestTrafo(TestCase):

    filename = "out.json"

    def test_se_existe_json(self):
        dirs = os.listdir()
        import ipdb
        ipdb.set_trace()
        self.assertIn(self.filename, dirs, "Nao existe o objeto JSON")

