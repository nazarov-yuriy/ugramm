import unittest
import json
from libs.dummy_engine import DummyEngine


class TestDummyEngine(unittest.TestCase):
    def test_noop(self):
        engine = DummyEngine()
        check_res = engine.check("We love contributions!")
        json_text = json.dumps(check_res.serialize(), sort_keys=True)
        expected = '{"fixed": "We love contributions!", "matches": [], "version": "dummy 0.1"}'
        self.assertEqual(json_text, expected)

    def test_minimal(self):
        engine = DummyEngine()
        check_res = engine.check("Don't need a consolidation agreement so we don't have to negotiate one.")
        json_text = json.dumps(check_res.serialize(), sort_keys=True)
        expected = '{"fixed": "Don\'t need a consolidation agreement, so we don\'t have to negotiate one.", ' \
                   '"matches": [{"length": 0, "message": null, "quickfix": ",", "rule": null, "start": 36}], ' \
                   '"version": "dummy 0.1"}'
        self.assertEqual(json_text, expected)
