import unittest
import json
from libs.base_engine import Match, CheckResult


class TestBaseEngine(unittest.TestCase):
    def test_match(self):
        match = Match(36, 0, quickfix=",")
        json_text = json.dumps(match.serialize(), sort_keys=True)
        expected = '{"length": 0, "message": null, "quickfix": ",", "rule": null, "start": 36}'
        self.assertEqual(json_text, expected)

    def test_check_result(self):
        check_res = CheckResult("test")
        match = Match(5, 0, quickfix=",")
        check_res.matches.append(match)
        check_res.fill_fixed("fixed text")

        json_text = json.dumps(check_res.serialize(), sort_keys=True)
        expected = '{"fixed": "fixed, text", "matches": [{"length": 0, "message": null, "quickfix": ",", ' \
                   '"rule": null, "start": 5}], "version": "test"}'
        self.assertEqual(json_text, expected)

    def test_check_result_assert(self):
        check_res = CheckResult("test")
        check_res.matches.append(Match(5, 0, quickfix=","))
        check_res.matches.append(Match(4, 0, quickfix=","))  # reordered fixes
        self.assertRaises(AssertionError, lambda: check_res.fill_fixed("fixed text"))
