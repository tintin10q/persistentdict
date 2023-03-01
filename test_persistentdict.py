import pickle
import unittest
import json
from persistentdict import persistentdict


class TestPersistentdict(unittest.TestCase):
    def tearDown(self) -> None:
        import os
        if os.path.exists("test.json"):
            os.remove("test.json")
        if os.path.exists("test.pickle"):
            os.remove("test.pickle")

    def test_json_write(self):
        with persistentdict("test", format=json) as d:
            d["a"] = 1
            d["b"] = {"b1": 2}
            d["c"] = 3
        with open("test.json", 'r') as f:
            self.assertEqual(json.load(f), {"a": 1, "b": {"b1": 2}, "c": 3})

    def test_json_read(self):
        with open("test.json", 'w+') as f:
            json.dump({"a": 1, "b": {"b1": 2}, "c": 3}, f)

        with open("test.json", 'r') as f:
            self.assertEqual(json.load(f), {"a": 1, "b": {"b1": 2}, "c": 3})

        with persistentdict("test", format=json) as d:
            self.assertEqual(d, {"a": 1, "b": {"b1": 2}, "c": 3})



if __name__ == '__main__':
    unittest.main()
